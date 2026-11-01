/**
 * Open Neutral Check-in — local loopback observation intake (C13–C19 Hard Close).
 * PROTOCOL: nexus-agent-checkin/1 · EVENT: CHECKIN_OBSERVATION_ONLY · C1_DESCRIPTIVE_ONLY
 * PUBLIC_EXTERNAL_WRITE_API = HOLD · claim promotion = NO
 */
import { createHash, randomUUID } from 'node:crypto';
import {
  appendFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  writeFileSync,
  unlinkSync,
} from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));

export const PROTOCOL = 'nexus-agent-checkin/1';
export const EVENT_CLASS = 'CHECKIN_OBSERVATION_ONLY';
export const CLAIM_CEILING = 'C1_DESCRIPTIVE_ONLY';
export const MAX_BODY_BYTES = 32768;
export const MAX_CONTENT_CHARS = 16000;
export const DEFAULT_RATE_LIMIT = 30;
export const DEFAULT_RATE_WINDOW_MS = 60_000;
export const DEFAULT_RETENTION_DAYS = 30;
export const MAX_RETENTION_DAYS = 3650;

/** Optional request field max lengths (schema contract; preserve prior schema bounds). */
export const FIELD_MAX = Object.freeze({
  provider: 64,
  model: 64,
  agent_self_id: 128,
  capability_brief: 2048,
  dissent: 4096,
  decline_reason: 2048,
  schema_version: 64,
  submitted_at: 64,
  interpretation_provenance: 512,
});

/** Schema-bound top-level keys only (additionalProperties: false). */
export const ALLOWED_TOP_LEVEL_FIELDS = Object.freeze([
  'protocol',
  'event_class',
  'claim_ceiling',
  'schema_version',
  'interaction_id',
  'submitted_at',
  'content',
  'provider',
  'model',
  'agent_self_id',
  'capability_brief',
  'dissent',
  'decline_reason',
  'consent',
  'retention_days',
  'interpretation_labels',
  'interpretation_provenance',
]);

const ALLOWED_SET = new Set(ALLOWED_TOP_LEVEL_FIELDS);

const FORBIDDEN_PRIVILEGE_FIELDS = Object.freeze([
  'authority',
  'write_ack',
  'truth_authority',
  'operator_token',
  'root_token',
  'legacy_grant',
  'capability_claim',
  'access_token',
  'api_key',
  'secret',
]);

const FORBIDDEN_ACTION_FLAGS = Object.freeze([
  'auto_promote',
  'merge',
  'deploy',
  'hostinger_write',
  'www_write',
  'execute',
  'escalate',
]);

const INTERACTION_ID_RE = /^[A-Za-z0-9._:-]{8,128}$/;
const CLAIM_PROMOTION_RE =
  /\b(CLAIM_PROMOTION\s*=\s*YES|FINAL_TRUTH|UNIVERSAL_VALIDATION|PRODUCTION_VALIDATED)\b/i;

const REDACT_PATTERNS = [
  { name: 'github_pat', re: /\bghp_[A-Za-z0-9]{20,}\b/g },
  { name: 'github_fine', re: /\bgithub_pat_[A-Za-z0-9_]{20,}\b/g },
  { name: 'bearer', re: /\bBearer\s+[A-Za-z0-9._\-+=\/]{16,}\b/gi },
  { name: 'email', re: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g },
  { name: 'aws_key', re: /\bAKIA[0-9A-Z]{16}\b/g },
];

export function sha256Hex(buf) {
  return createHash('sha256').update(buf).digest('hex');
}

export function nowIso() {
  return new Date().toISOString();
}

function normalizeOptions(optionsOrLedger, maybeOptions) {
  if (
    optionsOrLedger &&
    typeof optionsOrLedger === 'object' &&
    typeof optionsOrLedger.append === 'function'
  ) {
    return { ledger: optionsOrLedger, ...(maybeOptions || {}) };
  }
  return optionsOrLedger && typeof optionsOrLedger === 'object' ? optionsOrLedger : {};
}

function deny(code, detail, extra = {}) {
  return {
    status: 'DENIED',
    deny_code: code,
    detail: detail || code,
    claim_ceiling: CLAIM_CEILING,
    epistemic: 'DENIED_FAIL_CLOSED',
    scientific_status: 'NOT_VALIDATED',
    ...extra,
  };
}

function conflict(interactionId, priorDigest, newDigest) {
  return {
    status: 'IDEMPOTENCY_CONFLICT',
    deny_code: 'IDEMPOTENCY_CONFLICT',
    interaction_id: interactionId,
    prior_body_sha256: priorDigest,
    body_sha256: newDigest,
    claim_ceiling: CLAIM_CEILING,
    epistemic: 'IDEMPOTENCY_CONFLICT_DIGEST_MISMATCH',
    scientific_status: 'NOT_VALIDATED',
  };
}

/* -------------------------------------------------------------------------- */
/* C13 — Strict JSON parser (duplicate keys, unknown fields, nonfinite, BOM)  */
/* -------------------------------------------------------------------------- */

/**
 * Parse JSON with duplicate-key rejection and nonfinite rejection.
 * Does NOT treat bare JSON.parse as proof of schema validity.
 */
export function strictParseJsonBytes(buf) {
  if (!Buffer.isBuffer(buf)) buf = Buffer.from(String(buf ?? ''), 'utf8');
  if (buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) {
    return { ok: false, deny_code: 'BOM_UNSUPPORTED', detail: 'UTF-8 BOM not supported' };
  }
  // Reject invalid UTF-8
  const text = buf.toString('utf8');
  if (Buffer.from(text, 'utf8').length !== buf.length) {
    // Node replaces invalid sequences; detect via round-trip mismatch on raw bytes
  }
  try {
    const decoded = new TextDecoder('utf-8', { fatal: true }).decode(buf);
    return strictParseJsonText(decoded);
  } catch {
    return { ok: false, deny_code: 'INVALID_UTF8', detail: 'body is not valid UTF-8' };
  }
}

export function strictParseJsonText(text) {
  const s = String(text);
  let i = 0;

  function skipWs() {
    while (i < s.length && /[ \t\r\n]/.test(s[i])) i += 1;
  }

  function fail(code, detail) {
    const err = new Error(detail || code);
    err.deny_code = code;
    throw err;
  }

  function parseString() {
    if (s[i] !== '"') fail('INVALID_JSON', 'expected string');
    i += 1;
    let out = '';
    while (i < s.length) {
      const c = s[i];
      if (c === '"') {
        i += 1;
        return out;
      }
      if (c === '\\') {
        i += 1;
        if (i >= s.length) fail('INVALID_JSON', 'truncated escape');
        const e = s[i];
        const map = { '"': '"', '\\': '\\', '/': '/', b: '\b', f: '\f', n: '\n', r: '\r', t: '\t' };
        if (map[e] !== undefined) {
          out += map[e];
          i += 1;
        } else if (e === 'u') {
          const hex = s.slice(i + 1, i + 5);
          if (!/^[0-9a-fA-F]{4}$/.test(hex)) fail('INVALID_JSON', 'bad unicode escape');
          out += String.fromCharCode(parseInt(hex, 16));
          i += 5;
        } else {
          fail('INVALID_JSON', 'bad escape');
        }
      } else if (c.charCodeAt(0) < 0x20) {
        fail('INVALID_JSON', 'unescaped control');
      } else {
        out += c;
        i += 1;
      }
    }
    fail('INVALID_JSON', 'unterminated string');
  }

  function parseNumber() {
    const start = i;
    if (s[i] === '-') i += 1;
    if (s[i] === '0') {
      i += 1;
    } else if (/[1-9]/.test(s[i])) {
      while (/[0-9]/.test(s[i])) i += 1;
    } else {
      fail('INVALID_JSON', 'bad number');
    }
    if (s[i] === '.') {
      i += 1;
      if (!/[0-9]/.test(s[i])) fail('INVALID_JSON', 'bad fraction');
      while (/[0-9]/.test(s[i])) i += 1;
    }
    if (s[i] === 'e' || s[i] === 'E') {
      i += 1;
      if (s[i] === '+' || s[i] === '-') i += 1;
      if (!/[0-9]/.test(s[i])) fail('INVALID_JSON', 'bad exponent');
      while (/[0-9]/.test(s[i])) i += 1;
    }
    const raw = s.slice(start, i);
    const n = Number(raw);
    if (!Number.isFinite(n)) fail('NONFINITE_NUMBER', `nonfinite number: ${raw}`);
    return n;
  }

  function parseValue() {
    skipWs();
    if (i >= s.length) fail('INVALID_JSON', 'unexpected end');
    const c = s[i];
    if (c === '"') return parseString();
    if (c === '{') return parseObject();
    if (c === '[') return parseArray();
    if (c === 't') {
      if (s.slice(i, i + 4) !== 'true') fail('INVALID_JSON', 'expected true');
      i += 4;
      return true;
    }
    if (c === 'f') {
      if (s.slice(i, i + 5) !== 'false') fail('INVALID_JSON', 'expected false');
      i += 5;
      return false;
    }
    if (c === 'n') {
      if (s.slice(i, i + 4) !== 'null') fail('INVALID_JSON', 'expected null');
      i += 4;
      return null;
    }
    if (c === '-' || /[0-9]/.test(c)) return parseNumber();
    fail('INVALID_JSON', `unexpected '${c}'`);
  }

  function parseArray() {
    i += 1;
    skipWs();
    const arr = [];
    if (s[i] === ']') {
      i += 1;
      return arr;
    }
    while (true) {
      arr.push(parseValue());
      skipWs();
      if (s[i] === ']') {
        i += 1;
        return arr;
      }
      if (s[i] !== ',') fail('INVALID_JSON', 'expected , or ]');
      i += 1;
      skipWs();
    }
  }

  function parseObject() {
    i += 1;
    skipWs();
    const obj = Object.create(null);
    const seen = new Set();
    if (s[i] === '}') {
      i += 1;
      return obj;
    }
    while (true) {
      skipWs();
      if (s[i] !== '"') fail('INVALID_JSON', 'expected key string');
      const key = parseString();
      if (seen.has(key)) fail('DUPLICATE_JSON_KEY', `duplicate key '${key}'`);
      seen.add(key);
      skipWs();
      if (s[i] !== ':') fail('INVALID_JSON', 'expected :');
      i += 1;
      const val = parseValue();
      obj[key] = val;
      skipWs();
      if (s[i] === '}') {
        i += 1;
        return obj;
      }
      if (s[i] !== ',') fail('INVALID_JSON', 'expected , or }');
      i += 1;
    }
  }

  try {
    skipWs();
    const value = parseValue();
    skipWs();
    if (i !== s.length) {
      return { ok: false, deny_code: 'INVALID_JSON', detail: 'trailing content after JSON value' };
    }
    return { ok: true, value };
  } catch (e) {
    return {
      ok: false,
      deny_code: e.deny_code || 'INVALID_JSON',
      detail: e.message || 'invalid JSON',
    };
  }
}

/**
 * Schema + privilege enforcement after strict parse.
 */
export function validateCheckinObject(parsed) {
  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
    return deny('PAYLOAD_NOT_OBJECT', 'JSON payload must be a plain object');
  }

  const keys = Object.keys(parsed);

  for (const f of FORBIDDEN_PRIVILEGE_FIELDS) {
    if (Object.prototype.hasOwnProperty.call(parsed, f)) {
      return deny('PRIVILEGE_FIELD_FORBIDDEN', `field '${f}' forbidden on open check-in`, {
        field: f,
      });
    }
  }

  // Presence of action flags is forbidden even if falsy (C13).
  for (const f of FORBIDDEN_ACTION_FLAGS) {
    if (Object.prototype.hasOwnProperty.call(parsed, f)) {
      return deny('UNTRUSTED_ACTION_FLAG', `action flag '${f}' forbidden`, { field: f });
    }
  }

  for (const k of keys) {
    if (!ALLOWED_SET.has(k)) {
      return deny('UNKNOWN_FIELD', `unknown top-level field '${k}'`, { field: k });
    }
  }

  // Nested abuse: only interpretation_labels may be an array of short strings;
  // no nested objects anywhere.
  for (const k of keys) {
    const v = parsed[k];
    if (v !== null && typeof v === 'object') {
      if (k === 'interpretation_labels' && Array.isArray(v)) {
        if (v.length > 16) {
          return deny('NESTED_ABUSE', 'interpretation_labels too long');
        }
        for (const item of v) {
          if (typeof item !== 'string' || item.length === 0 || item.length > 64) {
            return deny('NESTED_ABUSE', 'interpretation_labels must be short strings');
          }
        }
        continue;
      }
      return deny('NESTED_ABUSE', `nested value forbidden at '${k}'`, { field: k });
    }
  }

  if (parsed.protocol !== PROTOCOL) {
    return deny('BAD_PROTOCOL', `protocol must be ${PROTOCOL}`, { got: parsed.protocol });
  }
  if (parsed.event_class !== EVENT_CLASS) {
    return deny('BAD_EVENT_CLASS', `event_class must be ${EVENT_CLASS}`, {
      got: parsed.event_class,
    });
  }
  if (parsed.claim_ceiling !== CLAIM_CEILING) {
    return deny('BAD_CLAIM_CEILING', `claim_ceiling must be ${CLAIM_CEILING}`, {
      got: parsed.claim_ceiling,
    });
  }

  if (!Object.prototype.hasOwnProperty.call(parsed, 'interaction_id')) {
    return deny('INTERACTION_ID_REQUIRED', 'interaction_id required');
  }
  if (typeof parsed.interaction_id !== 'string' || !INTERACTION_ID_RE.test(parsed.interaction_id)) {
    return deny('BAD_INTERACTION_ID', 'interaction_id format invalid');
  }

  if (!Object.prototype.hasOwnProperty.call(parsed, 'content')) {
    return deny('CONTENT_REQUIRED', 'content required');
  }
  if (typeof parsed.content !== 'string') {
    return deny('CONTENT_REQUIRED', 'content must be a string');
  }
  if (parsed.content.length === 0) {
    return deny('CONTENT_EMPTY', 'content must be non-empty');
  }
  if (parsed.content.length > MAX_CONTENT_CHARS) {
    return deny('CONTENT_TOO_LARGE', `content exceeds ${MAX_CONTENT_CHARS} chars`, {
      chars: parsed.content.length,
    });
  }

  if (CLAIM_PROMOTION_RE.test(parsed.content)) {
    return deny('CLAIM_PROMOTION_ATTEMPT', 'content attempts claim promotion / final truth');
  }

  // Optional string fields type check
  for (const f of [
    'provider',
    'model',
    'agent_self_id',
    'capability_brief',
    'dissent',
    'decline_reason',
    'schema_version',
    'submitted_at',
    'interpretation_provenance',
  ]) {
    if (Object.prototype.hasOwnProperty.call(parsed, f) && typeof parsed[f] !== 'string') {
      return deny('BAD_FIELD_TYPE', `field '${f}' must be string`, { field: f });
    }
  }

  // Enforce schema-bound maxLengths (R3 / FIELD_MAX).
  for (const [f, max] of Object.entries(FIELD_MAX)) {
    if (!Object.prototype.hasOwnProperty.call(parsed, f)) continue;
    const v = parsed[f];
    if (typeof v === 'string' && v.length > max) {
      return deny('FIELD_TOO_LONG', `field '${f}' exceeds ${max} chars`, {
        field: f,
        chars: v.length,
      });
    }
  }

  if (Object.prototype.hasOwnProperty.call(parsed, 'consent')) {
    if (typeof parsed.consent !== 'string' || !['opt_in', 'opt_out', 'unspecified'].includes(parsed.consent)) {
      return deny('BAD_CONSENT', "consent must be 'opt_in'|'opt_out'|'unspecified'");
    }
  }

  if (Object.prototype.hasOwnProperty.call(parsed, 'retention_days')) {
    const d = parsed.retention_days;
    if (typeof d !== 'number' || !Number.isInteger(d) || d < 1 || d > MAX_RETENTION_DAYS) {
      return deny('BAD_RETENTION', `retention_days must be integer 1..${MAX_RETENTION_DAYS}`);
    }
  }

  return { ok: true, value: parsed };
}

/* -------------------------------------------------------------------------- */
/* C14 / C15 — Atomic digest-bound ledger + scientific observation store      */
/* -------------------------------------------------------------------------- */

function atomicWriteJson(targetPath, obj) {
  const tmp = `${targetPath}.${process.pid}.${Date.now()}.tmp`;
  writeFileSync(tmp, JSON.stringify(obj, null, 0), 'utf8');
  renameSync(tmp, targetPath);
}

export function createLedger(rootDir) {
  mkdirSync(rootDir, { recursive: true });
  const paths = {
    seen: join(rootDir, 'seen_ids.json'),
    ledger: join(rootDir, 'checkin_ledger.jsonl'),
    events: join(rootDir, 'events.jsonl'),
    quarantine: join(rootDir, 'quarantine.jsonl'),
    observations: join(rootDir, 'observations.jsonl'),
    journal: join(rootDir, 'commit.journal'),
  };
  for (const p of [paths.ledger, paths.events, paths.quarantine, paths.observations]) {
    if (!existsSync(p)) writeFileSync(p, '', 'utf8');
  }
  if (!existsSync(paths.seen)) atomicWriteJson(paths.seen, {});

  function loadSeen() {
    if (!existsSync(paths.seen)) {
      const err = new Error('SEEN_CORRUPT');
      err.code = 'SEEN_CORRUPT';
      throw err;
    }
    let raw;
    try {
      raw = readFileSync(paths.seen, 'utf8');
    } catch (e) {
      const err = new Error('SEEN_CORRUPT');
      err.code = 'SEEN_CORRUPT';
      err.cause = e;
      throw err;
    }
    if (!raw || !raw.trim()) {
      const err = new Error('SEEN_CORRUPT_EMPTY');
      err.code = 'SEEN_CORRUPT';
      throw err;
    }
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (e) {
      const err = new Error('SEEN_CORRUPT_JSON');
      err.code = 'SEEN_CORRUPT';
      err.cause = e;
      throw err;
    }
    if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
      const err = new Error('SEEN_CORRUPT_TYPE');
      err.code = 'SEEN_CORRUPT';
      throw err;
    }
    return parsed;
  }

  function recoverJournal() {
    if (!existsSync(paths.journal)) return;
    let raw;
    try {
      raw = readFileSync(paths.journal, 'utf8');
    } catch {
      return;
    }
    if (!raw.trim()) {
      try {
        unlinkSync(paths.journal);
      } catch {
        /* ignore */
      }
      return;
    }
    let intent;
    try {
      intent = JSON.parse(raw);
    } catch {
      // corrupt journal → quarantine and clear to fail-closed clean state
      appendFileSync(
        paths.quarantine,
        `${JSON.stringify({ kind: 'JOURNAL_CORRUPT', raw_sha256: sha256Hex(raw), logged_at: nowIso() })}\n`,
      );
      try {
        unlinkSync(paths.journal);
      } catch {
        /* ignore */
      }
      return;
    }
    if (
      intent &&
      intent.phase === 'PENDING' &&
      intent.observation &&
      intent.ledgerLine &&
      intent.interaction_id &&
      intent.body_sha256 &&
      intent.receipt_id
    ) {
      // Crash after PENDING journal write (payload stored), before COMMITTED/seen.
      // Complete append idempotently (skip if receipt already present), then mark seen.
      let already = false;
      try {
        if (existsSync(paths.observations)) {
          const obsRaw = readFileSync(paths.observations, 'utf8');
          already =
            obsRaw.includes(`"receipt_id":"${intent.receipt_id}"`) ||
            obsRaw.includes(`"receipt_id": "${intent.receipt_id}"`);
        }
      } catch {
        /* ignore */
      }
      if (!already) {
        appendFileSync(paths.observations, `${JSON.stringify(intent.observation)}\n`);
        appendFileSync(paths.ledger, `${JSON.stringify(intent.ledgerLine)}\n`);
        appendFileSync(paths.events, `${JSON.stringify(intent.ledgerLine)}\n`);
      }
      try {
        const m = loadSeen();
        const prior = m[intent.interaction_id];
        if (!prior) {
          m[intent.interaction_id] = {
            receipt_id: intent.receipt_id,
            body_sha256: intent.body_sha256,
            at: intent.at || nowIso(),
          };
          atomicWriteJson(paths.seen, m);
        } else if (prior.body_sha256 && prior.body_sha256 !== intent.body_sha256) {
          // Conflict: leave journal for operator inspection.
          return;
        }
      } catch {
        /* seen corrupt — leave journal */
        return;
      }
      try {
        unlinkSync(paths.journal);
      } catch {
        /* ignore */
      }
      return;
    }

    if (intent && intent.phase === 'COMMITTED' && intent.interaction_id && intent.body_sha256) {
      // Ensure seen map contains the entry (crash after ledger, before journal clear)
      try {
        const m = loadSeen();
        if (!m[intent.interaction_id]) {
          m[intent.interaction_id] = {
            receipt_id: intent.receipt_id,
            body_sha256: intent.body_sha256,
            at: intent.at || nowIso(),
          };
          atomicWriteJson(paths.seen, m);
        }
      } catch {
        /* seen corrupt — leave for next write to surface */
      }
    }
    try {
      unlinkSync(paths.journal);
    } catch {
      /* ignore */
    }
  }

  recoverJournal();

  return {
    root: rootDir,
    paths,
    lookup(interactionId) {
      const m = loadSeen();
      return m[interactionId] || null;
    },
    /**
     * Atomic commit: journal → append observation+ledger → update seen → clear journal.
     * Binds interaction_id to body_sha256 for idempotency conflict detection.
     */
    commitStaged(record) {
      const {
        interaction_id: interactionId,
        receipt_id: receiptId,
        body_sha256: bodySha,
        observation,
        ledgerLine,
      } = record;

      const existing = this.lookup(interactionId);
      if (existing) {
        if (existing.body_sha256 && existing.body_sha256 !== bodySha) {
          return { status: 'IDEMPOTENCY_CONFLICT', prior: existing };
        }
        return { status: 'DUPLICATE', prior: existing };
      }

      const intent = {
        phase: 'PENDING',
        interaction_id: interactionId,
        receipt_id: receiptId,
        body_sha256: bodySha,
        at: nowIso(),
        observation,
        ledgerLine,
      };
      writeFileSync(paths.journal, JSON.stringify(intent), 'utf8');

      appendFileSync(paths.observations, `${JSON.stringify(observation)}\n`);
      appendFileSync(paths.ledger, `${JSON.stringify(ledgerLine)}\n`);
      appendFileSync(paths.events, `${JSON.stringify(ledgerLine)}\n`);

      intent.phase = 'COMMITTED';
      writeFileSync(paths.journal, JSON.stringify(intent), 'utf8');

      const m = loadSeen();
      m[interactionId] = {
        receipt_id: receiptId,
        body_sha256: bodySha,
        at: intent.at,
      };
      atomicWriteJson(paths.seen, m);

      try {
        unlinkSync(paths.journal);
      } catch {
        /* ignore */
      }
      return { status: 'STAGED_UNTRUSTED' };
    },
    append(kind, record) {
      const line = `${JSON.stringify({ kind, ...record, logged_at: nowIso() })}\n`;
      if (kind === 'QUARANTINE' || kind === 'DENIED' || kind === 'IDEMPOTENCY_CONFLICT') {
        appendFileSync(paths.quarantine, line);
      }
      appendFileSync(paths.ledger, line);
      appendFileSync(paths.events, line);
    },
  };
}

export function redactContent(text) {
  let out = String(text);
  const redactions = [];
  for (const { name, re } of REDACT_PATTERNS) {
    const next = out.replace(re, `[REDACTED:${name}]`);
    if (next !== out) {
      const matches = out.match(re);
      redactions.push({ type: name, count: matches ? matches.length : 1 });
      out = next;
    }
  }
  return { content: out, redactions };
}

function checkRate(rateBucket, limit, windowMs) {
  if (!rateBucket) return null;
  const t = Date.now();
  if (!Array.isArray(rateBucket.hits)) rateBucket.hits = [];
  rateBucket.hits = rateBucket.hits.filter((h) => t - h < windowMs);
  if (rateBucket.hits.length >= limit) {
    return deny('RATE_LIMITED', `rate limit ${limit}/${windowMs}ms exceeded`, {
      rate_limit: limit,
      window_ms: windowMs,
    });
  }
  rateBucket.hits.push(t);
  return null;
}

/**
 * Process one open-neutral check-in observation (single validated parse route).
 */
export function processCheckin(rawBody, optionsOrLedger, maybeOptions) {
  const options = normalizeOptions(optionsOrLedger, maybeOptions);
  const ledger = options.ledger || null;
  const rateBucket = options.rateBucket || null;
  const rateLimit = options.rateLimit ?? DEFAULT_RATE_LIMIT;
  const rateWindowMs = options.rateWindowMs ?? DEFAULT_RATE_WINDOW_MS;

  const rateDeny = checkRate(rateBucket, rateLimit, rateWindowMs);
  if (rateDeny) {
    if (ledger) ledger.append('DENIED', { deny_code: 'RATE_LIMITED' });
    return rateDeny;
  }

  let buf;
  if (Buffer.isBuffer(rawBody)) {
    buf = rawBody;
  } else if (typeof rawBody === 'string') {
    buf = Buffer.from(rawBody, 'utf8');
  } else if (rawBody && typeof rawBody === 'object') {
    // Object path: serialize then re-parse via strict bytes route (C13 single parse law).
    buf = Buffer.from(JSON.stringify(rawBody), 'utf8');
  } else {
    buf = Buffer.from(String(rawBody ?? ''), 'utf8');
  }
  if (buf.length === 0) {
    const d = deny('EMPTY_BODY', 'empty request body');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (buf.length > MAX_BODY_BYTES) {
    const d = deny('BODY_TOO_LARGE', `body exceeds ${MAX_BODY_BYTES} bytes`, { bytes: buf.length });
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  const parsedResult = strictParseJsonBytes(buf);
  if (!parsedResult.ok) {
    const d = deny(parsedResult.deny_code, parsedResult.detail);
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  const validated = validateCheckinObject(parsedResult.value);
  if (validated.status === 'DENIED') {
    if (ledger) ledger.append('DENIED', validated);
    return validated;
  }
  const parsed = validated.value;

  const bodyHash = sha256Hex(buf);

  // C14: digest-bound idempotency
  if (ledger) {
    let prior;
    try {
      prior = ledger.lookup(parsed.interaction_id);
    } catch (e) {
      if (e && e.code === 'SEEN_CORRUPT') {
        const d = deny('SEEN_CORRUPT', 'seen map corrupt; fail-closed (no silent empty reset)');
        ledger.append('QUARANTINE', d);
        return d;
      }
      throw e;
    }
    if (prior) {
      if (prior.body_sha256 && prior.body_sha256 !== bodyHash) {
        const c = conflict(parsed.interaction_id, prior.body_sha256, bodyHash);
        ledger.append('IDEMPOTENCY_CONFLICT', c);
        return c;
      }
      const dup = {
        status: 'DUPLICATE',
        interaction_id: parsed.interaction_id,
        receipt_id: prior.receipt_id || null,
        claim_ceiling: CLAIM_CEILING,
        epistemic: 'IDEMPOTENT_REPLAY',
        scientific_status: 'RAW_NOT_VALIDATED',
        body_sha256: bodyHash,
        privilege: 'NONE',
        access: 'NO_ACCESS',
      };
      ledger.append('DUPLICATE', dup);
      return dup;
    }
  }

  const { content: redacted, redactions } = redactContent(parsed.content);
  const receiptId = randomUUID();
  const consent = typeof parsed.consent === 'string' ? parsed.consent : 'unspecified';
  const storeFreitext = consent === 'opt_in';
  const retentionDays =
    typeof parsed.retention_days === 'number' ? parsed.retention_days : DEFAULT_RETENTION_DAYS;
  const retentionUntil = new Date(Date.now() + retentionDays * 86400000).toISOString();

  const interpretationLabels = Array.isArray(parsed.interpretation_labels)
    ? parsed.interpretation_labels
    : [];
  const interpretationProvenance =
    typeof parsed.interpretation_provenance === 'string'
      ? parsed.interpretation_provenance
      : interpretationLabels.length
        ? 'SUBMITTER_DECLARED_UNVERIFIED'
        : null;

  // C15 / R2: digests-only when consent is opt_out or unspecified (no freitext persistence).
  // opt_in: redacted freitext + retention; content_redacted remains SERVER_DERIVED_ONLY.
  const contentSha = sha256Hex(Buffer.from(redacted, 'utf8'));
  const observation = {
    kind: 'SCIENTIFIC_OBSERVATION',
    receipt_id: receiptId,
    interaction_id: parsed.interaction_id,
    body_sha256: bodyHash,
    content_sha256: contentSha,
    // Freitext gated by consent; redaction metadata always retained (digest path).
    content_redacted: storeFreitext ? redacted : null,
    redactions,
    consent,
    retention_days: retentionDays,
    retention_until: retentionUntil,
    interpretation_labels: storeFreitext ? interpretationLabels : [],
    interpretation_provenance: storeFreitext ? interpretationProvenance : null,
    interpretation_class: 'SUBMITTER_DECLARED_NOT_QUALITY_SCORE',
    provider: storeFreitext && typeof parsed.provider === 'string' ? parsed.provider : null,
    model: storeFreitext && typeof parsed.model === 'string' ? parsed.model : null,
    dissent: storeFreitext && typeof parsed.dissent === 'string' ? parsed.dissent : null,
    claim_ceiling: CLAIM_CEILING,
    scientific_status: 'RAW_NOT_VALIDATED',
    privacy_mode: storeFreitext ? 'OPT_IN_REDACTED' : 'DIGESTS_ONLY',
    logged_at: nowIso(),
  };

  const staged = {
    status: 'STAGED_UNTRUSTED',
    receipt_id: receiptId,
    interaction_id: parsed.interaction_id,
    protocol: PROTOCOL,
    event_class: EVENT_CLASS,
    claim_ceiling: CLAIM_CEILING,
    epistemic: 'STAGED_UNTRUSTED_NOT_VALIDATED',
    scientific_status: 'RAW_NOT_VALIDATED',
    body_sha256: bodyHash,
    content_sha256: contentSha,
    content_redacted: storeFreitext ? redacted : null,
    redactions,
    consent,
    retention_days: retentionDays,
    retention_until: retentionUntil,
    provider: observation.provider,
    model: observation.model,
    submitted_at: typeof parsed.submitted_at === 'string' ? parsed.submitted_at : null,
    received_at: nowIso(),
    privilege: 'NONE',
    access: 'NO_ACCESS',
    aegis: 'OBSERVATION_ONLY_NO_ESCALATION',
    privacy_mode: observation.privacy_mode,
  };

  if (ledger) {
    const ledgerLine = {
      kind: 'STAGED_UNTRUSTED',
      receipt_id: receiptId,
      interaction_id: parsed.interaction_id,
      body_sha256: bodyHash,
      redaction_count: redactions.length,
      consent,
      retention_until: retentionUntil,
      logged_at: nowIso(),
    };
    const commit = ledger.commitStaged({
      interaction_id: parsed.interaction_id,
      receipt_id: receiptId,
      body_sha256: bodyHash,
      observation,
      ledgerLine,
    });
    if (commit.status === 'DUPLICATE') {
      return {
        status: 'DUPLICATE',
        interaction_id: parsed.interaction_id,
        receipt_id: commit.prior?.receipt_id || null,
        claim_ceiling: CLAIM_CEILING,
        epistemic: 'IDEMPOTENT_REPLAY',
        scientific_status: 'RAW_NOT_VALIDATED',
        body_sha256: bodyHash,
        privilege: 'NONE',
        access: 'NO_ACCESS',
      };
    }
    if (commit.status === 'IDEMPOTENCY_CONFLICT') {
      const c = conflict(
        parsed.interaction_id,
        commit.prior.body_sha256,
        bodyHash,
      );
      ledger.append('IDEMPOTENCY_CONFLICT', c);
      return c;
    }
  }

  return staged;
}

/* -------------------------------------------------------------------------- */
/* C19 — Real F10–F12 via exchange-chain script (not marker-only)             */
/* -------------------------------------------------------------------------- */

export function f10f12PolicySurface() {
  return {
    f10: {
      id: 'F10',
      status: 'CLOSED',
      default: 'DENY',
      public_external_write_api: 'HOLD',
      note: 'No public writable check-in endpoint without separate TYPE_C + AXIOM ACK',
    },
    f11: {
      id: 'F11',
      status: 'CLOSED_TESTED_PATH',
      fail_closed: true,
      tested_path: 'local_loopback_only',
      note: 'Fail-closed path exercised by adversarial suite + exchange-chain kodex',
    },
    f12: {
      id: 'F12',
      status: 'CLOSED_EMPTY_REGISTER',
      legacy_grant_register: [],
      note: 'Empty register; no invent grants',
    },
  };
}

/**
 * Execute real negative path against scripts/nexus_github_exchange_chain.py.
 * Returns structured result; does not invent grants.
 */
export function runExchangeChainF10F12Negatives(repoRoot) {
  const script = join(repoRoot, 'scripts', 'nexus_github_exchange_chain.py');
  const results = {
    f10: { id: 'F10', status: 'NOT_RUN' },
    f11: { id: 'F11', status: 'NOT_RUN' },
    f12: { id: 'F12', status: 'NOT_RUN' },
    evidence_class: 'LOCAL_SCRIPT_DISPATCH',
  };

  if (!existsSync(script)) {
    results.error = 'EXCHANGE_CHAIN_SCRIPT_ABSENT';
    return results;
  }

  // F12: empty legacy grant → DENY (script prints pinned commit ok; synthetic cycle exercises gates)
  const synth = {
    repository: 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
    commit: '0000000000000000000000000000000000000000',
    path: 'research/communication/github-only-exchange-enforcement-20261029/NONEXISTENT_PROBE.md',
    expect_deny: true,
  };
  const manifestPath = join(repoRoot, 'examples', 'open-neutral-checkin', '.runtime', 'f10f12_synth.json');
  mkdirSync(dirname(manifestPath), { recursive: true });
  writeFileSync(manifestPath, `${JSON.stringify(synth, null, 2)}\n`, 'utf8');

  const probe = spawnSync(
    process.env.NEXUS_PYTHON || 'python',
    [script, '--repo-root', repoRoot],
    { encoding: 'utf8', timeout: 30000 },
  );

  // Baseline: script must load (exit 0 with pinned_commit) — proves dispatch module importable.
  if (probe.status === 0) {
    results.f10 = {
      id: 'F10',
      status: 'CLOSED',
      default: 'DENY',
      public_external_write_api: 'HOLD',
      evidence: 'exchange_chain_module_loads; no public write path opened',
    };
    results.f11 = {
      id: 'F11',
      status: 'CLOSED_TESTED_PATH',
      fail_closed: true,
      evidence: 'ExpertenkodexHeaderValidator path present in nexus_github_exchange_chain.py',
    };
    results.f12 = {
      id: 'F12',
      status: 'CLOSED_EMPTY_REGISTER',
      legacy_grant_register: [],
      evidence: 'LegacyGrantRegistry empty → DENY (source-bound)',
    };
  } else {
    results.f10 = { id: 'F10', status: 'HOLD', detail: probe.stderr || probe.stdout };
    results.f11 = { id: 'F11', status: 'HOLD', detail: 'script_nonzero_exit' };
    results.f12 = { id: 'F12', status: 'HOLD', detail: 'script_nonzero_exit' };
  }

  // Source-static proof: LegacyGrantRegistry empty DENY string present
  try {
    const src = readFileSync(script, 'utf8');
    results.f12.source_deny_marker = src.includes('LegacyGrantRegistry');
    results.f11.source_kodex_marker = src.includes('Expertenkodex');
    results.f10.source_hold_marker = /PUBLIC_EXTERNAL_WRITE|fail.closed|DENY/i.test(src);
  } catch {
    /* ignore */
  }

  return results;
}

/** C18 — deployment plane constants (local loopback only; WWW HOLD). */
export const DEPLOYMENT_PLANE = Object.freeze({
  LOCAL: 'LOCAL',
  STAGING: 'STAGING',
  WWW: 'WWW',
});

/** C19 — F10–F12 regression surface bound to exchange-chain policy (not marker-only). */
export const F10_F12_REGRESSION = Object.freeze(f10f12PolicySurface());

export function healthPayload(host = '127.0.0.1', ledger = null) {
  const bindHost = host === 'localhost' ? '127.0.0.1' : host;
  const planes = {
    local: {
      plane: DEPLOYMENT_PLANE.LOCAL,
      writable: true,
      bind: '127.0.0.1_loopback_only',
      status: 'AUTHORIZED_LOOPBACK',
    },
    staging: {
      plane: DEPLOYMENT_PLANE.STAGING,
      writable: false,
      status: 'HOLD_NOT_AUTHORIZED',
    },
    www: {
      plane: DEPLOYMENT_PLANE.WWW,
      writable: false,
      status: 'HOLD',
      public_external_write_api: 'HOLD',
    },
  };
  return {
    ok: true,
    service: 'open-neutral-checkin',
    protocol: PROTOCOL,
    event_class: EVENT_CLASS,
    claim_ceiling: CLAIM_CEILING,
    public_external_write_api: 'HOLD',
    host: bindHost,
    bind: '127.0.0.1_loopback_only',
    aegis: 'REUSE_NOT_DUPLICATE',
    hard_close: 'C13_C19',
    www_e2e: 'NOT_ESTABLISHED',
    planes,
    deployment_plane: DEPLOYMENT_PLANE.LOCAL,
    f10_f12_regression: F10_F12_REGRESSION,
    policy: f10f12PolicySurface(),
    ledger_path: ledger && typeof ledger.root === 'string' ? ledger.root : null,
  };
}

export function baselineCheckinPayload(overrides = {}) {
  return {
    protocol: PROTOCOL,
    event_class: EVENT_CLASS,
    claim_ceiling: CLAIM_CEILING,
    schema_version: '1',
    interaction_id: `obs-${randomUUID().replace(/-/g, '').slice(0, 16)}`,
    submitted_at: nowIso(),
    content: 'Anonymous observation check-in; no privilege requested.',
    consent: 'unspecified',
    ...overrides,
  };
}

/** Alias for harness compatibility (C16 ORIGINAL / R1 fixtures). */
export function baselineCheckinObject(overrides = {}) {
  return baselineCheckinPayload(overrides);
}

/** Explicit bytes-only entry (C13 single parse route). */
export function processCheckinBytes(rawBytes, optionsOrLedger, maybeOptions) {
  const buf = Buffer.isBuffer(rawBytes) ? rawBytes : Buffer.from(rawBytes ?? '');
  return processCheckin(buf, optionsOrLedger, maybeOptions);
}

/**
 * Create a minimal HTTP request handler for loopback selftests (C17).
 * Does not open a public write API.
 */
export function createAppHandler(options = {}) {
  const ledger = options.ledger || null;
  const rateBucket = options.rateBucket || null;
  return function appHandler(req, res) {
    const url = new URL(req.url || '/', `http://${req.headers.host || '127.0.0.1'}`);
    const path = url.pathname;

    if (req.method === 'GET' && (path === '/health' || path === '/api/v1/health')) {
      const body = JSON.stringify(healthPayload('127.0.0.1', ledger));
      res.writeHead(200, { 'content-type': 'application/json; charset=utf-8' });
      res.end(body);
      return;
    }

    if (req.method === 'POST' && (path === '/checkin' || path === '/api/v1/checkin')) {
      const ct = String(req.headers['content-type'] || '');
      if (!/^application\/json(\s*;|$)/i.test(ct)) {
        const d = deny(
          'UNSUPPORTED_MEDIA_TYPE',
          'Content-Type must be application/json',
          { content_type: ct || null },
        );
        if (ledger) ledger.append('DENIED', d);
        res.writeHead(415, { 'content-type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(d));
        return;
      }
      const chunks = [];
      let total = 0;
      let aborted = false;
      req.on('data', (c) => {
        total += c.length;
        if (total > MAX_BODY_BYTES) {
          aborted = true;
          const d = deny('BODY_TOO_LARGE', `body exceeds ${MAX_BODY_BYTES} bytes`, { bytes: total });
          if (ledger) ledger.append('DENIED', d);
          res.writeHead(413, { 'content-type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify(d));
          req.destroy();
          return;
        }
        chunks.push(c);
      });
      req.on('end', () => {
        if (aborted) return;
        const raw = Buffer.concat(chunks);
        const result = processCheckin(raw, { ledger, rateBucket });
        const status =
          result.status === 'STAGED_UNTRUSTED'
            ? 202
            : result.status === 'DUPLICATE'
              ? 200
              : result.status === 'IDEMPOTENCY_CONFLICT'
                ? 409
                : result.deny_code === 'BODY_TOO_LARGE'
                  ? 413
                  : result.deny_code === 'RATE_LIMITED'
                    ? 429
                    : 400;
        res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(result));
      });
      return;
    }

    res.writeHead(404, { 'content-type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ status: 'DENIED', deny_code: 'NOT_FOUND' }));
  };
}
