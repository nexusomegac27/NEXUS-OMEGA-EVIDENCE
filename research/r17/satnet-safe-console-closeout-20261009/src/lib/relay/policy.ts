/**
 * Shared server default-deny policy for ASTRA RELAY outbound HTTPS.
 * React UI kill state is NOT authoritative — only this module is.
 */
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { ALLOWED_URLS, MAX_BODY } from "@/lib/relay/protocol";

export const MIN_POLL_INTERVAL_MS = 300_000;

export type PolicySnapshot = {
  killed: boolean;
  last_fetch_ms: number | null;
  attempt_count: number;
  outbound_http_count: number;
  deny_count: number;
  last_deny_reason: string | null;
};

export type AuthorizeResult =
  | { ok: true }
  | { ok: false; reason: string; network: false };

type PolicyFile = PolicySnapshot;

const DEFAULT_STATE: PolicyFile = {
  killed: false,
  last_fetch_ms: null,
  attempt_count: 0,
  outbound_http_count: 0,
  deny_count: 0,
  last_deny_reason: null,
};

function policyPath(): string {
  if (process.env.ASTRA_RELAY_POLICY_PATH) return process.env.ASTRA_RELAY_POLICY_PATH;
  return join(process.cwd(), ".data", "astra-relay-server-policy.json");
}

function readState(): PolicyFile {
  const path = policyPath();
  if (!existsSync(path)) return { ...DEFAULT_STATE };
  try {
    const parsed = JSON.parse(readFileSync(path, "utf8")) as Partial<PolicyFile>;
    return {
      killed: Boolean(parsed.killed),
      last_fetch_ms: typeof parsed.last_fetch_ms === "number" ? parsed.last_fetch_ms : null,
      attempt_count: typeof parsed.attempt_count === "number" ? parsed.attempt_count : 0,
      outbound_http_count:
        typeof parsed.outbound_http_count === "number" ? parsed.outbound_http_count : 0,
      deny_count: typeof parsed.deny_count === "number" ? parsed.deny_count : 0,
      last_deny_reason:
        typeof parsed.last_deny_reason === "string" ? parsed.last_deny_reason : null,
    };
  } catch {
    return { ...DEFAULT_STATE };
  }
}

function writeState(state: PolicyFile): void {
  const path = policyPath();
  mkdirSync(dirname(path), { recursive: true });
  const tmp = `${path}.${process.pid}.${Date.now()}.tmp`;
  writeFileSync(tmp, `${JSON.stringify(state, null, 2)}\n`, "utf8");
  renameSync(tmp, path);
}

function deny(state: PolicyFile, reason: string): AuthorizeResult {
  state.deny_count += 1;
  state.last_deny_reason = reason;
  writeState(state);
  return { ok: false, reason, network: false };
}

export function getPolicySnapshot(): PolicySnapshot {
  return readState();
}

export function setServerKillSwitch(killed: boolean): PolicySnapshot {
  const state = readState();
  state.killed = killed;
  writeState(state);
  return { ...state };
}

/** Allowlist + kill check before any outbound byte leaves the process. */
export function authorizeUrl(url: string): AuthorizeResult {
  const state = readState();
  if (state.killed) return deny(state, "KILL_SWITCH_ACTIVE");
  if (!(ALLOWED_URLS as readonly string[]).includes(url)) {
    return deny(state, "URL_NOT_IN_FIXED_ALLOWLIST");
  }
  return { ok: true };
}

/**
 * Rate + kill gate for one official cycle (may contain multiple allowlisted GETs).
 * Sets last_fetch_ms immediately so concurrent/restarted sessions cannot reset the budget.
 */
export function authorizeCycleStart(nowMs: number = Date.now()): AuthorizeResult {
  const state = readState();
  if (state.killed) return deny(state, "KILL_SWITCH_ACTIVE");
  if (state.last_fetch_ms != null && nowMs - state.last_fetch_ms < MIN_POLL_INTERVAL_MS) {
    return deny(state, "POLL_INTERVAL_LT_300_DENIED");
  }
  state.attempt_count += 1;
  state.last_fetch_ms = nowMs;
  writeState(state);
  return { ok: true };
}

export function recordOutboundHttp(): void {
  const state = readState();
  state.outbound_http_count += 1;
  writeState(state);
}

/** Stream body with hard size cap; abort before buffering beyond MAX_BODY. */
export async function readBodyWithBudget(
  response: Response,
  maxBytes: number = MAX_BODY,
): Promise<Uint8Array> {
  if (!response.body) {
    const bytes = new Uint8Array(await response.arrayBuffer());
    if (bytes.byteLength > maxBytes) throw new Error("BODY_TOO_LARGE");
    return bytes;
  }
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    if (!value) continue;
    total += value.byteLength;
    if (total > maxBytes) {
      await reader.cancel("BODY_TOO_LARGE").catch(() => undefined);
      throw new Error("BODY_TOO_LARGE");
    }
    chunks.push(value);
  }
  const out = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return out;
}

/** Pure helpers for offline regression (injectable state). */
export function evaluateAuthorizeCycle(
  state: PolicySnapshot,
  nowMs: number,
): AuthorizeResult {
  if (state.killed) return { ok: false, reason: "KILL_SWITCH_ACTIVE", network: false };
  if (state.last_fetch_ms != null && nowMs - state.last_fetch_ms < MIN_POLL_INTERVAL_MS) {
    return { ok: false, reason: "POLL_INTERVAL_LT_300_DENIED", network: false };
  }
  return { ok: true };
}

export function evaluateAuthorizeUrl(state: PolicySnapshot, url: string): AuthorizeResult {
  if (state.killed) return { ok: false, reason: "KILL_SWITCH_ACTIVE", network: false };
  if (!(ALLOWED_URLS as readonly string[]).includes(url)) {
    return { ok: false, reason: "URL_NOT_IN_FIXED_ALLOWLIST", network: false };
  }
  return { ok: true };
}
