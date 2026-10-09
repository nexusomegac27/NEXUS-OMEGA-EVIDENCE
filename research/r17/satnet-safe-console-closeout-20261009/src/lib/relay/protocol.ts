export const NODE_URN = "urn:nexus-omega:node:astra-relay:v1";
export const XRAYS_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json";
export const SOURCES_URL = "https://services.swpc.noaa.gov/json/goes/instrument-sources.json";
export const USER_AGENT = "NEXUS-ASTRA-RELAY/0.1 (science read-only; low-frequency)";
export const CLAIM_CEILING = "C1_DESCRIPTIVE_ONLY";
export const MAX_BODY = 1_000_000;
export const STALE_SECONDS = 1800;
export const FUTURE_SECONDS = 300;

export const ALLOWED_URLS = [XRAYS_URL, SOURCES_URL] as const;

export type XrayPoint = {
  time: string;
  short: number | null;
  long: number | null;
};

export type Observation = {
  source_class: "SATELLITE_SENSOR_VIA_OFFICIAL_INTERNET_API";
  instrument: "GOES_XRS_REPORTED";
  satellite_reported: number;
  energy: string;
  time_tag: string;
  flux: number;
  unit: "W/m^2";
  source_id: "NOAA_SWPC_GOES_PRIMARY_XRAYS";
  quality_flag: string;
  observed_flux: number | null;
  electron_correction: number | null;
  electron_contaminaton: boolean | null;
  node_urn: typeof NODE_URN;
  record_id: string;
};

export type Transfer = {
  record_id: string;
  time_tag: string;
  satellite: number;
  energy: string;
  flux: number;
  payload_sha256: string;
  consumer_ack_sha256: string;
  readback_sha256: string;
  transfer_utc: string;
  raw_sha256: string;
  mode: "SMOKE_ONLY";
  duplicate: boolean;
};

export type InstrumentCell = { primary: number | null; secondary: number | null };

export type MappingInfo = {
  url: typeof SOURCES_URL;
  raw_sha256: string;
  raw_bytes: number;
  time_tag: string | null;
  instruments: { name: string; primary: number | null; secondary: number | null }[];
};

export type XrayMeta = {
  url: typeof XRAYS_URL;
  http_status: number;
  raw_sha256: string;
  raw_bytes: number;
  headers_subset: Record<string, string>;
};

export type ReportedSample = {
  time_tag: string;
  flux: number;
  satellite: number;
  energy: string;
};

export type CycleResult = {
  ok: boolean;
  error: string | null;
  at_utc: string;
  mode: "SMOKE_ONLY";
  claim_ceiling: typeof CLAIM_CEILING;
  surface: "ARCHITECT_PREVIEW_NOT_TYPE_C";
  elite_operational: "NOT_CERTIFIED_BY_AUTOMATED_EVALUATOR";
  direct_rf_link: false;
  runtime: "TEST_STARTED_NOT_PASS";
  qualified: boolean;
  rejected_rows: number;
  rejection_reasons: Record<string, number>;
  qualified_unique: number;
  errors: string[];
  points: XrayPoint[];
  fresh: Observation[];
  transfers: Transfer[];
  new_accepted: number;
  duplicate_accepted: number;
  latest_long: Observation | null;
  latest_short: Observation | null;
  reported_latest_long: ReportedSample | null;
  reported_latest_short: ReportedSample | null;
  mapping: MappingInfo | null;
  xrays: XrayMeta | null;
  consumer_note: string;
};

export type ProbeKind = "foreign-url" | "poll-under-300" | "realtest-without-authority";

export type ProbeResult = {
  refused: string;
  detail: string;
  network: false;
};

export const RETURN_INDEX = [
  "ASTRA_R16_D4_HOST_AUTHORITY_AND_BOUNDARY.json",
  "ASTRA_R16_D4_SOURCE_EXACT_NOAA_PREFLIGHT.md",
  "ASTRA_R16_D4_B2_LOCAL_TESTS.txt",
  "ASTRA_R16_D4_B3_SMOKE_RUN.json",
  "ASTRA_R16_D4_24H_RUN_META_AND_LOGS",
  "ASTRA_R16_D4_SECOND_CONSUMER_EVIDENCE.json",
  "ASTRA_R16_D4_NEGATIVE_CONTROL_MATRIX.md",
  "ASTRA_R16_D4_RECOVERY_AND_KILL_SWITCH.md",
  "ASTRA_R16_D4_INDEPENDENT_WITNESS_RETURN.md",
  "ASTRA_BIRTH_LAW_STAGE_AND_ELITE_QUALIFICATION_DELTA.json",
  "ASTRA_R16_D4_AXIOM_ADJUDICATION_HANDOFF.md",
  "OUTPUT_HASH_MANIFEST.json",
] as const;

export const SOURCE_LEDGER = [
  {
    id: "NO-01",
    href: "https://www.swpc.noaa.gov/content/data-access",
    note: "Öffentlicher JSON-Zugang, Identität des Quellenbetreibers.",
    gate: "Kontext",
  },
  {
    id: "NO-02",
    href: "https://www.swpc.noaa.gov/products/goes-x-ray-flux",
    note: "GOES-XRS, 1-Minuten-Mittel, Primär-/Sekundärwechsel, Kalibrierung.",
    gate: "Kontext",
  },
  {
    id: "NO-03",
    href: XRAYS_URL,
    note: "Einzige Messreihe dieser Fläche. Schema wird bei jeder Lesung geprüft.",
    gate: "Allowlist",
  },
  {
    id: "NO-04",
    href: SOURCES_URL,
    note: "Instrument → gemeldeter Satellit. Bytes und UTC werden festgehalten.",
    gate: "Allowlist",
  },
  {
    id: "NO-05",
    href: "https://services.swpc.noaa.gov/json/goes/primary/",
    note: "Andere Produkte. Kein automatisches Failover.",
    gate: "Gesperrt",
  },
  {
    id: "SA-01",
    href: "https://docs.satnogs.org/projects/satnogs-network/en/latest/api.html",
    note: "SatNOGS, CC BY-SA. Kein eigenes RF.",
    gate: "Nicht dieser Test",
  },
  {
    id: "CE-01",
    href: "https://celestrak.org/NORAD/documentation/gp-data-formats.php",
    note: "Bahnelemente. Keine Sensorwerte.",
    gate: "Nicht dieser Test",
  },
] as const;

export const BIRTH_LADDER = [
  { id: "B0_CONCEIVED", text: "Nur ein Name. Keine stabile Knotenidentität." },
  { id: "B1_FOUNDATION_BOUND", text: "Rolle und Identität sind kanonisch gebunden." },
  { id: "B2_ARTIFACT_BORN", text: "Prüfsummen-gebundenes Paket existiert." },
  { id: "B3_OPERATIONALLY_BORN", text: "Begrenztes Laufzeitverhalten ist belegt." },
  { id: "B4_PUBLICLY_BORN", text: "Öffentliche Fläche unabhängig zurückgelesen." },
  { id: "B5_CONTINUITY_WITNESSED", text: "Primary, Secondary und unabhängiger Witness." },
] as const;

export const INVARIANTS = [
  ["CAPABILITY", "AUTHORITY"],
  ["SOURCE", "TRUTH"],
  ["SCHEMA_VALID", "CLAIM_VALID"],
  ["SELF_REPORT", "INDEPENDENT_VALIDATION"],
  ["ANALOGY", "EVIDENCE"],
  ["HYPOTHESIS", "FINDING"],
  ["OBSERVATION", "CAUSAL_PROOF"],
  ["BIRTH_REGISTERED", "SCIENTIFICALLY_VALIDATED"],
  ["PUBLIC_ROUTE", "AUTONOMY"],
] as const;

export const CHECK_LABELS: Record<string, string> = {
  REALTEST_NOT_SMOKE: "Lauf ist Realtest, nicht nur eine Leseprobe.",
  COMPLETE_REAL_24H: "Mind. 24 Stunden echte Laufzeit.",
  POLLS_95_PERCENT: "Mindestens 95 % der Zyklen ohne Fehler qualifiziert.",
  EACH_6H_WINDOW_NEW_OBSERVATIONS: "In jedem 6-Stunden-Fenster eine neue Realtest-Zeile.",
  AT_LEAST_4_DISTINCT_RECORDS: "Mindestens vier verschiedene Datensätze.",
  NO_UNEXPLAINED_GAP_OVER_60_MIN: "Kein Poll-Abstand über 60 Minuten.",
  CONSUMER_ACK_READBACK_VERIFIED: "Nutzlast, Quittung und Rücklesen tragen denselben SHA-256.",
  COMPLETED: "Schleife ohne äußeren Abbruch beendet.",
};

const BANDS = [
  { letter: "A", floor: 1e-8 },
  { letter: "B", floor: 1e-7 },
  { letter: "C", floor: 1e-6 },
  { letter: "M", floor: 1e-5 },
  { letter: "X", floor: 1e-4 },
] as const;

export function flareClass(flux: number): { letter: string; scale: number; label: string } | null {
  if (!Number.isFinite(flux) || flux < 0) return null;
  let chosen: (typeof BANDS)[number] = BANDS[0];
  if (flux < BANDS[0].floor) {
    chosen = BANDS[0];
  } else {
    for (const band of BANDS) {
      if (flux >= band.floor) chosen = band;
    }
  }
  const scale = flux / chosen.floor;
  return { letter: chosen.letter, scale, label: `${chosen.letter}${scale.toFixed(1)}` };
}

export function formatStamp(t: Date): string {
  return t.toISOString().replace(".000Z", "Z");
}

export function formatFlux(n: number): string {
  if (!Number.isFinite(n)) return "—";
  return n.toExponential(3);
}

export function formatAge(seconds: number): string {
  if (!Number.isFinite(seconds)) return "—";
  const s = Math.max(0, Math.round(seconds));
  if (s < 90) return `${s} s`;
  const m = Math.round(s / 60);
  if (m < 120) return `${m} min`;
  const h = Math.floor(m / 60);
  const rem = m % 60;
  if (h < 48) return rem === 0 ? `${h} h` : `${h} h ${rem} min`;
  const d = Math.floor(h / 24);
  const rh = h % 24;
  return rh === 0 ? `${d} d` : `${d} d ${rh} h`;
}

export function parseTime(s: unknown): Date {
  if (typeof s !== "string") throw new Error("NO_TIME_TAG");
  if (!/(Z|[+-]\d{2}:\d{2})$/.test(s)) throw new Error("NO_TIMEZONE");
  const t = new Date(s);
  if (Number.isNaN(t.getTime())) throw new Error("NO_TIME_TAG");
  return t;
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(sortValue(value));
}

function sortValue(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortValue);
  if (value && typeof value === "object") {
    const source = value as Record<string, unknown>;
    const out: Record<string, unknown> = {};
    for (const key of Object.keys(source).sort()) out[key] = sortValue(source[key]);
    return out;
  }
  return value;
}

export async function sha256Text(s: string): Promise<string> {
  return sha256Bytes(new TextEncoder().encode(s));
}

export async function sha256Bytes(bytes: Uint8Array): Promise<string> {
  const copy = new Uint8Array(bytes.byteLength);
  copy.set(bytes);
  const digest = await crypto.subtle.digest("SHA-256", copy);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function normalize(row: unknown, now: Date): Promise<Observation> {
  if (!row || typeof row !== "object" || Array.isArray(row)) throw new Error("NON_OBJECT");
  const record = row as Record<string, unknown>;
  for (const key of ["time_tag", "satellite", "flux", "energy"] as const) {
    if (!(key in record)) throw new Error(`MISSING_${key}`);
  }
  const t = parseTime(record.time_tag);
  if ((t.getTime() - now.getTime()) / 1000 > FUTURE_SECONDS) throw new Error("FUTURE_TIME");
  if ((now.getTime() - t.getTime()) / 1000 > STALE_SECONDS) throw new Error("STALE_30MIN");
  const sat = record.satellite;
  if (typeof sat !== "number" || !Number.isInteger(sat) || sat < 1 || sat > 99999) {
    throw new Error("INVALID_SATELLITE");
  }
  const energy = record.energy;
  if (typeof energy !== "string" || energy.length < 1 || energy.length > 64) {
    throw new Error("INVALID_ENERGY");
  }
  const flux = record.flux;
  if (typeof flux !== "number" || !Number.isFinite(flux) || flux < 0) throw new Error("INVALID_FLUX");
  const time_tag = formatStamp(t);
  const record_id = await sha256Text(`GOES_XRS|${sat}|${energy}|${time_tag}`);
  let quality_flag = "NOT_PRESENT_IN_XRAYS_FIELDS";
  if ("quality_flag" in record) {
    quality_flag = typeof record.quality_flag === "string" ? record.quality_flag : canonicalJson(record.quality_flag);
  }
  return {
    source_class: "SATELLITE_SENSOR_VIA_OFFICIAL_INTERNET_API",
    instrument: "GOES_XRS_REPORTED",
    satellite_reported: sat,
    energy,
    time_tag,
    flux,
    unit: "W/m^2",
    source_id: "NOAA_SWPC_GOES_PRIMARY_XRAYS",
    quality_flag,
    observed_flux: typeof record.observed_flux === "number" ? record.observed_flux : null,
    electron_correction: typeof record.electron_correction === "number" ? record.electron_correction : null,
    electron_contaminaton: typeof record.electron_contaminaton === "boolean" ? record.electron_contaminaton : null,
    node_urn: NODE_URN,
    record_id,
  };
}

export function chartPoints(rows: Record<string, unknown>[]): XrayPoint[] {
  const byTime = new Map<string, XrayPoint>();
  for (const row of rows) {
    if (typeof row.time_tag !== "string" || typeof row.flux !== "number" || !Number.isFinite(row.flux) || row.flux <= 0) {
      continue;
    }
    const slot = byTime.get(row.time_tag) ?? { time: row.time_tag, short: null, long: null };
    if (row.energy === "0.05-0.4nm") slot.short = row.flux;
    if (row.energy === "0.1-0.8nm") slot.long = row.flux;
    byTime.set(row.time_tag, slot);
  }
  return [...byTime.values()].sort((a, b) => a.time.localeCompare(b.time));
}

export function reportedLatest(rows: Record<string, unknown>[], energy: string): ReportedSample | null {
  let best: ReportedSample | null = null;
  for (const row of rows) {
    if (row.energy !== energy) continue;
    if (typeof row.time_tag !== "string" || typeof row.flux !== "number" || typeof row.satellite !== "number") continue;
    if (!best || row.time_tag > best.time_tag) {
      best = { time_tag: row.time_tag, flux: row.flux, satellite: row.satellite, energy };
    }
  }
  return best;
}

export type EvalEvent = { at_utc: string; qualified: boolean; errors: string[] };
export type EvalObs = {
  record_id: string;
  transfer_utc: string;
  mode: string;
  payload_sha256: string;
  consumer_ack_sha256: string;
  readback_sha256: string;
};

export type Evaluation = {
  verdict: "HOLD_NO_POLLS" | "HOLD_INCOMPLETE" | "CANDIDATE_REQUIRES_INDEPENDENT_WITNESS";
  checks: Record<string, boolean>;
  cycles: number;
  qualified_cycles: number;
  qualified_ratio: number | null;
  distinct_observations: number;
  new_transfer_count: number;
  windows_6h_new_records: number[];
  max_poll_gap_s: number | null;
  real_elapsed_hours: number;
  claim_ceiling: typeof CLAIM_CEILING;
  direct_rf_link: false;
  elite_operational: "NOT_CERTIFIED_BY_AUTOMATED_EVALUATOR";
};

export function evaluateSession(input: {
  mode: "SMOKE_ONLY" | "REALTEST_24H_CANDIDATE";
  start_utc: string;
  elapsed_hours: number;
  events: EvalEvent[];
  observations: EvalObs[];
  completed: boolean;
}): Evaluation {
  const base = {
    claim_ceiling: "C1_DESCRIPTIVE_ONLY",
    direct_rf_link: false,
    elite_operational: "NOT_CERTIFIED_BY_AUTOMATED_EVALUATOR",
  } as const;
  if (input.events.length === 0) {
    return {
      ...base,
      verdict: "HOLD_NO_POLLS",
      checks: {},
      cycles: 0,
      qualified_cycles: 0,
      qualified_ratio: null,
      distinct_observations: 0,
      new_transfer_count: 0,
      windows_6h_new_records: [0, 0, 0, 0],
      max_poll_gap_s: null,
      real_elapsed_hours: input.elapsed_hours,
    };
  }
  const start = parseTime(input.start_utc);
  const successes = input.events.filter((event) => event.qualified && event.errors.length === 0).length;
  const ratio = successes / input.events.length;
  const realObs = input.observations.filter((row) => row.mode === "REALTEST_24H_CANDIDATE");
  const windows = [0, 1, 2, 3].map((k) => {
    const lo = start.getTime() + 6 * k * 3600_000;
    const hi = lo + 6 * 3600_000;
    return realObs.filter((row) => {
      const t = parseTime(row.transfer_utc).getTime();
      return t >= lo && t < hi;
    }).length;
  });
  const pollTimes = input.events.map((event) => parseTime(event.at_utc).getTime());
  const gaps: number[] = [];
  for (let i = 1; i < pollTimes.length; i++) gaps.push((pollTimes[i] - pollTimes[i - 1]) / 1000);
  const checks: Record<string, boolean> = {
    REALTEST_NOT_SMOKE: input.mode === "REALTEST_24H_CANDIDATE",
    COMPLETE_REAL_24H: input.elapsed_hours >= 24,
    POLLS_95_PERCENT: ratio >= 0.95,
    EACH_6H_WINDOW_NEW_OBSERVATIONS: windows.every((n) => n >= 1),
    AT_LEAST_4_DISTINCT_RECORDS: new Set(input.observations.map((row) => row.record_id)).size >= 4,
    NO_UNEXPLAINED_GAP_OVER_60_MIN: input.events.length > 1 && (gaps.length ? Math.max(...gaps) : 1e9) <= 3600,
    CONSUMER_ACK_READBACK_VERIFIED:
      input.observations.length > 0 &&
      input.observations.every(
        (row) => row.payload_sha256 === row.consumer_ack_sha256 && row.consumer_ack_sha256 === row.readback_sha256,
      ),
    COMPLETED: input.completed,
  };
  const pass = Object.values(checks).every(Boolean);
  return {
    ...base,
    verdict: pass ? "CANDIDATE_REQUIRES_INDEPENDENT_WITNESS" : "HOLD_INCOMPLETE",
    checks,
    cycles: input.events.length,
    qualified_cycles: successes,
    qualified_ratio: Math.round(ratio * 1_000_000) / 1_000_000,
    distinct_observations: new Set(input.observations.map((row) => row.record_id)).size,
    new_transfer_count: input.observations.length,
    windows_6h_new_records: windows,
    max_poll_gap_s: gaps.length ? Math.max(...gaps) : null,
    real_elapsed_hours: input.elapsed_hours,
  };
}

export function emptyCycle(at: string, error: string | null): CycleResult {
  return {
    ok: false,
    error,
    at_utc: at,
    mode: "SMOKE_ONLY",
    claim_ceiling: CLAIM_CEILING,
    surface: "ARCHITECT_PREVIEW_NOT_TYPE_C",
    elite_operational: "NOT_CERTIFIED_BY_AUTOMATED_EVALUATOR",
    direct_rf_link: false,
    runtime: "TEST_STARTED_NOT_PASS",
    qualified: false,
    rejected_rows: 0,
    rejection_reasons: {},
    qualified_unique: 0,
    errors: error ? [error] : [],
    points: [],
    fresh: [],
    transfers: [],
    new_accepted: 0,
    duplicate_accepted: 0,
    latest_long: null,
    latest_short: null,
    reported_latest_long: null,
    reported_latest_short: null,
    mapping: null,
    xrays: null,
    consumer_note:
      "In-Prozess-Ledger dieser Serverinstanz. Kein SQLite, kein 127.0.0.1:18773, kein unabhängiger Zeuge.",
  };
}
