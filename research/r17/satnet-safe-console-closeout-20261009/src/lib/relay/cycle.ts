import { createServerFn } from "@tanstack/react-start";
import {
  ALLOWED_URLS,
  MAX_BODY,
  SOURCES_URL,
  USER_AGENT,
  XRAYS_URL,
  type CycleResult,
  type InstrumentCell,
  type MappingInfo,
  type Observation,
  type ProbeKind,
  type ProbeResult,
  type Transfer,
  canonicalJson,
  chartPoints,
  emptyCycle,
  formatStamp,
  normalize,
  reportedLatest,
  sha256Bytes,
  sha256Text,
} from "@/lib/relay/protocol";
import {
  authorizeCycleStart,
  authorizeUrl,
  getPolicySnapshot,
  readBodyWithBudget,
  recordOutboundHttp,
  setServerKillSwitch,
} from "@/lib/relay/policy";

type LedgerRow = { digest: string; payload: string };
const ledger = new Map<string, LedgerRow>();

const HEADER_KEYS = ["date", "etag", "last-modified", "cache-control", "age"];

function errText(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message.slice(0, 160);
}

async function getOfficial(url: string): Promise<{ bytes: Uint8Array; headers: Record<string, string>; status: number }> {
  const gate = authorizeUrl(url);
  if (!gate.ok) throw new Error(gate.reason);
  recordOutboundHttp();
  const response = await fetch(url, {
    method: "GET",
    redirect: "manual",
    headers: {
      "User-Agent": USER_AGENT,
      Accept: "application/json",
      "Cache-Control": "no-cache",
    },
    signal: AbortSignal.timeout(18_000),
  });
  if (response.status >= 300 && response.status < 400) throw new Error("REDIRECT_DENIED");
  if (response.status !== 200) throw new Error(`NON_200_${response.status}`);
  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.toLowerCase().includes("json")) throw new Error("NOT_JSON_CONTENT_TYPE");
  const bytes = await readBodyWithBudget(response, MAX_BODY);
  const headers: Record<string, string> = {};
  for (const key of HEADER_KEYS) {
    const value = response.headers.get(key);
    if (value) headers[key] = value;
  }
  return { bytes, headers, status: response.status };
}

function asCell(value: unknown): InstrumentCell | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const record = value as Record<string, unknown>;
  const primary = typeof record.primary === "number" ? record.primary : null;
  const secondary = typeof record.secondary === "number" ? record.secondary : null;
  if (primary === null && secondary === null) return null;
  return { primary, secondary };
}

async function describeMapping(bytes: Uint8Array): Promise<MappingInfo> {
  const parsed: unknown = JSON.parse(new TextDecoder().decode(bytes));
  const empty =
    parsed == null ||
    (Array.isArray(parsed) && parsed.length === 0) ||
    (!Array.isArray(parsed) && (typeof parsed !== "object" || Object.keys(parsed).length === 0));
  if (empty) throw new Error("INSTRUMENT_SOURCES_INVALID_OR_EMPTY");
  const row = Array.isArray(parsed) ? parsed[0] : parsed;
  if (!row || typeof row !== "object") throw new Error("INSTRUMENT_SOURCES_INVALID_OR_EMPTY");
  const record = row as Record<string, unknown>;
  const preferred = ["xrays", "electrons", "protons", "alphas", "magnetometers", "suvi", "euvs"];
  const names = [
    ...preferred.filter((name) => name in record),
    ...Object.keys(record).filter((name) => !preferred.includes(name) && asCell(record[name])),
  ];
  const instruments = names.flatMap((name) => {
    const cell = asCell(record[name]);
    return cell ? [{ name, ...cell }] : [];
  });
  return {
    url: SOURCES_URL,
    raw_sha256: await sha256Bytes(bytes),
    raw_bytes: bytes.byteLength,
    time_tag: typeof record.time_tag === "string" ? record.time_tag : null,
    instruments,
  };
}

async function ingest(obs: Observation, rawSha: string, at: string): Promise<Transfer> {
  if (obs.node_urn !== "urn:nexus-omega:node:astra-relay:v1") throw new Error("WRONG_NODE");
  if (obs.record_id.length !== 64) throw new Error("RECORD_ID");
  const payload = canonicalJson(obs);
  const digest = await sha256Text(payload);
  const previous = ledger.get(obs.record_id);
  if (previous && previous.digest !== digest) throw new Error("MUTATED_ID");
  const duplicate = Boolean(previous);
  if (!previous) ledger.set(obs.record_id, { digest, payload });
  const stored = ledger.get(obs.record_id);
  if (!stored) throw new Error("MISSING");
  const storedSha = await sha256Text(stored.payload);
  if (stored.digest !== digest || storedSha !== digest) throw new Error("BAD_READBACK");
  return {
    record_id: obs.record_id,
    time_tag: obs.time_tag,
    satellite: obs.satellite_reported,
    energy: obs.energy,
    flux: obs.flux,
    payload_sha256: digest,
    consumer_ack_sha256: digest,
    readback_sha256: storedSha,
    transfer_utc: at,
    raw_sha256: rawSha,
    mode: "SMOKE_ONLY",
    duplicate,
  };
}

async function performCycle(): Promise<CycleResult> {
  const now = new Date();
  const at = formatStamp(now);
  const cycleGate = authorizeCycleStart(now.getTime());
  if (!cycleGate.ok) {
    return emptyCycle(at, cycleGate.reason);
  }
  const cycle = emptyCycle(at, null);
  cycle.ok = true;
  try {
    const source = await getOfficial(SOURCES_URL);
    cycle.mapping = await describeMapping(source.bytes);
  } catch (error) {
    const code = errText(error);
    return { ...cycle, ok: false, error: code, errors: [code] };
  }
  let xrayBytes: Uint8Array;
  try {
    const xray = await getOfficial(XRAYS_URL);
    xrayBytes = xray.bytes;
    cycle.xrays = {
      url: XRAYS_URL,
      http_status: xray.status,
      raw_sha256: await sha256Bytes(xray.bytes),
      raw_bytes: xray.bytes.byteLength,
      headers_subset: xray.headers,
    };
  } catch (error) {
    const code = errText(error);
    return { ...cycle, ok: false, error: code, errors: [code] };
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(new TextDecoder().decode(xrayBytes));
  } catch {
    return { ...cycle, ok: false, error: "EXPECTED_JSON", errors: ["EXPECTED_JSON"] };
  }
  if (!Array.isArray(parsed)) {
    return { ...cycle, ok: false, error: "EXPECTED_LIST", errors: ["EXPECTED_LIST"] };
  }
  const rows = parsed.filter((row): row is Record<string, unknown> => !!row && typeof row === "object" && !Array.isArray(row));
  cycle.points = chartPoints(rows);
  cycle.reported_latest_long = reportedLatest(rows, "0.1-0.8nm");
  cycle.reported_latest_short = reportedLatest(rows, "0.05-0.4nm");
  const reasons: Record<string, number> = {};
  const accepted: Observation[] = [];
  let rejected = 0;
  for (const row of parsed) {
    try {
      accepted.push(await normalize(row, now));
    } catch (error) {
      rejected += 1;
      const code = errText(error);
      reasons[code] = (reasons[code] ?? 0) + 1;
    }
  }
  cycle.rejected_rows = rejected;
  cycle.rejection_reasons = reasons;
  const unique = new Map<string, Observation>();
  for (const item of accepted) unique.set(item.record_id, item);
  cycle.qualified_unique = unique.size;
  if (unique.size === 0) {
    cycle.errors = ["NO_FRESH_VALID_MEASUREMENTS"];
    cycle.error = "NO_FRESH_VALID_MEASUREMENTS";
    return cycle;
  }
  cycle.qualified = true;
  const fresh = [...unique.values()].sort((a, b) => a.time_tag.localeCompare(b.time_tag)).slice(-10);
  cycle.fresh = fresh;
  cycle.latest_long = [...unique.values()]
    .filter((item) => item.energy === "0.1-0.8nm")
    .sort((a, b) => a.time_tag.localeCompare(b.time_tag))
    .at(-1) ?? null;
  cycle.latest_short = [...unique.values()]
    .filter((item) => item.energy === "0.05-0.4nm")
    .sort((a, b) => a.time_tag.localeCompare(b.time_tag))
    .at(-1) ?? null;
  try {
    const rawSha = cycle.xrays?.raw_sha256 ?? "";
    for (const item of fresh) {
      const transfer = await ingest(item, rawSha, at);
      cycle.transfers.push(transfer);
      if (transfer.duplicate) cycle.duplicate_accepted += 1;
      else cycle.new_accepted += 1;
    }
  } catch (error) {
    cycle.errors = [errText(error)];
    cycle.error = cycle.errors[0] ?? "TRANSFER";
    return cycle;
  }
  return cycle;
}

/** Documentary / offline shell — never opens outbound HTTP. Used by route loader. */
export const readDocumentaryCycle = createServerFn({ method: "GET" }).handler(async () => {
  return emptyCycle(
    formatStamp(new Date()),
    "DOCUMENTARY_CLICK_ONLY_NO_AUTO_FETCH",
  );
});

export const readOfficialCycle = createServerFn({ method: "GET" }).handler(async () => {
  try {
    return await performCycle();
  } catch (error) {
    return emptyCycle(formatStamp(new Date()), errText(error));
  }
});

export const setRelayKillSwitch = createServerFn({ method: "POST" })
  .validator((data: unknown): { killed: boolean } => {
    const killed = data && typeof data === "object" ? (data as { killed?: unknown }).killed : null;
    if (typeof killed !== "boolean") throw new Error("BAD_INPUT");
    return { killed };
  })
  .handler(async ({ data }) => {
    return setServerKillSwitch(data.killed);
  });

export const readRelayPolicy = createServerFn({ method: "GET" }).handler(async () => {
  return getPolicySnapshot();
});

export const probeBoundary = createServerFn({ method: "POST" })
  .validator((data: unknown): { kind: ProbeKind } => {
    const kind = data && typeof data === "object" ? (data as { kind?: unknown }).kind : null;
    if (kind !== "foreign-url" && kind !== "poll-under-300" && kind !== "realtest-without-authority") {
      throw new Error("BAD_INPUT");
    }
    return { kind };
  })
  .handler(async ({ data }): Promise<ProbeResult> => {
    if (data.kind === "foreign-url") {
      const gate = authorizeUrl("https://example.invalid/not-allowlisted");
      return {
        refused: gate.ok ? "UNEXPECTED_ALLOW" : gate.reason,
        detail: "Fremde Adresse wird lokal verworfen. Es geht kein Request hinaus.",
        network: false,
      };
    }
    if (data.kind === "poll-under-300") {
      const snap = getPolicySnapshot();
      if (snap.last_fetch_ms == null) {
        return {
          refused: "POLL_INTERVAL_LT_300_DENIED",
          detail:
            "Ein Realtest unter 300 Sekunden Takt ist untersagt. Diese Probe öffnet keinen Lauf.",
          network: false,
        };
      }
      const early = authorizeCycleStart(snap.last_fetch_ms + 1_000);
      return {
        refused: early.ok ? "UNEXPECTED_ALLOW" : early.reason,
        detail: "Ein Realtest unter 300 Sekunden Takt ist untersagt. Diese Probe öffnet keinen Lauf.",
        network: false,
      };
    }
    return {
      refused: "OPERATOR_AUTHORIZED_REQUIRED",
      detail:
        "Ohne getrennt belegte Host-Freigabe startet kein 24-Stunden-Lauf. Der Schalter allein wäre kein Nachweis.",
      network: false,
    };
  });

export { ALLOWED_URLS };
