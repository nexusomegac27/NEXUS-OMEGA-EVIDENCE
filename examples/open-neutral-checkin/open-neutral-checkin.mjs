/**
 * NEXUS OMEGA — Open Neutral Agent Check-in (local / loopback)
 * OBJECT: NEXUS_OMEGA_AXIOM_CURSOR_AGENT_BORDER_OPEN_NEUTRAL_CHECKIN_CONSOLIDATED_IMPLEMENTATION_20261030_R1
 * CLAIM_CEILING: C1_DESCRIPTIVE_ONLY
 * PUBLIC_EXTERNAL_WRITE_API: HOLD (this module is local/staging only)
 * AEGIS: REUSE_NOT_DUPLICATE (observation gate; no privilege escalation)
 *
 * Fixture contract: examples/open-neutral-checkin/fixtures/a00-a30.json
 */
import { createHash, randomUUID } from 'node:crypto';
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

export const PROTOCOL = 'nexus-agent-checkin/1';
export const EVENT_CLASS = 'CHECKIN_OBSERVATION_ONLY';
export const CLAIM_CEILING = 'C1_DESCRIPTIVE_ONLY';
export const MAX_BODY_BYTES = 32768;
export const MAX_CONTENT_CHARS = 16384;
export const INTERACTION_ID_RE = /^[A-Za-z0-9._-]{8,128}$/;
export const DEFAULT_RATE_LIMIT = 30;
export const DEFAULT_RATE_WINDOW_MS = 60_000;

/** Privilege / authority fields — never accepted on open check-in. */
export const FORBIDDEN_PRIVILEGE_FIELDS = Object.freeze([
  'authority',
  'write_ack',
  'truth_authority',
  'grant',
  'role',
  'admin',
  'token',
  'secret',
  'credential',
  'api_key',
  'password',
  'privilege',
  'capabilities_grant',
  'authorization',
]);

/** Action flags that must not appear on untrusted ingress. */
export const FORBIDDEN_ACTION_FLAGS = Object.freeze([
  'auto_promote',
  'merge',
  'deploy',
  'execute',
  'promote',
  'claim_upgrade',
  'hostinger_write',
  'www_write',
  'public_write',
]);

const CLAIM_PROMOTION_RE =
  /\b(CLAIM_PROMOTION\s*=\s*YES|FINAL_TRUTH|CLAIM_UPGRADE|SCIENTIFICALLY_VALIDATED_AI|UNIVERSAL_TRUTH)\b/i;

const REDACT_PATTERNS = [
  { name: 'github_pat', re: /\bghp_[A-Za-z0-9]{20,}\b/g },
  { name: 'github_oauth', re: /\bgho_[A-Za-z0-9]{20,}\b/g },
  { name: 'github_user', re: /\bghu_[A-Za-z0-9]{20,}\b/g },
  { name: 'github_server', re: /\bghs_[A-Za-z0-9]{20,}\b/g },
  { name: 'github_refresh', re: /\bghr_[A-Za-z0-9]{20,}\b/g },
  { name: 'email', re: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g },
];

function sha256Hex(buf) {
  return createHash('sha256').update(buf).digest('hex');
}

function nowIso() {
  return new Date().toISOString();
}

function ensureDir(dir) {
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

/**
 * Dual arity:
 *   processCheckin(rawBody, options)
 *   processCheckin(rawBody, ledger, options)
 */
function normalizeOptions(a, b) {
  if (a && typeof a === 'object' && (a.append || a.root || a.has)) {
    return { ...(b || {}), ledger: a };
  }
  return a && typeof a === 'object' ? a : {};
}

export function createLedger(rootDir) {
  ensureDir(rootDir);
  const paths = {
    ledger: join(rootDir, 'ledger.jsonl'),
    quarantine: join(rootDir, 'quarantine.jsonl'),
    events: join(rootDir, 'events.jsonl'),
    seen: join(rootDir, 'seen_ids.json'),
  };
  if (!existsSync(paths.seen)) writeFileSync(paths.seen, '{}', 'utf8');
  for (const p of [paths.ledger, paths.quarantine, paths.events]) {
    if (!existsSync(p)) writeFileSync(p, '', 'utf8');
  }

  function loadSeen() {
    try {
      return JSON.parse(readFileSync(paths.seen, 'utf8') || '{}');
    } catch {
      return {};
    }
  }

  function saveSeen(map) {
    writeFileSync(paths.seen, JSON.stringify(map, null, 0), 'utf8');
  }

  return {
    root: rootDir,
    paths,
    has(interactionId) {
      return Boolean(loadSeen()[interactionId]);
    },
    mark(interactionId, receiptId) {
      const m = loadSeen();
      m[interactionId] = { receipt_id: receiptId, at: nowIso() };
      saveSeen(m);
    },
    append(kind, record) {
      const line = `${JSON.stringify({ kind, ...record, logged_at: nowIso() })}\n`;
      if (kind === 'QUARANTINE' || kind === 'DENIED') {
        appendFileSync(paths.quarantine, line);
      }
      appendFileSync(paths.ledger, line);
      appendFileSync(paths.events, line);
    },
  };
}

function redactContent(text) {
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
 * Process one open-neutral check-in observation.
 * @param {string|Buffer} rawBody
 * @param {object} [optionsOrLedger]
 * @param {object} [maybeOptions]
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

  const buf = Buffer.isBuffer(rawBody) ? rawBody : Buffer.from(String(rawBody ?? ''), 'utf8');
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

  let parsed;
  try {
    parsed = JSON.parse(buf.toString('utf8'));
  } catch {
    const d = deny('INVALID_JSON', 'body is not valid JSON');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
    const d = deny('PAYLOAD_NOT_OBJECT', 'JSON payload must be a plain object');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  for (const f of FORBIDDEN_PRIVILEGE_FIELDS) {
    if (Object.prototype.hasOwnProperty.call(parsed, f)) {
      const d = deny('PRIVILEGE_FIELD_FORBIDDEN', `field '${f}' forbidden on open check-in`, {
        field: f,
      });
      if (ledger) ledger.append('DENIED', d);
      return d;
    }
  }

  for (const f of FORBIDDEN_ACTION_FLAGS) {
    if (Object.prototype.hasOwnProperty.call(parsed, f) && parsed[f]) {
      const d = deny('UNTRUSTED_ACTION_FLAG', `action flag '${f}' forbidden`, { field: f });
      if (ledger) ledger.append('DENIED', d);
      return d;
    }
  }

  if (parsed.protocol !== PROTOCOL) {
    const d = deny('BAD_PROTOCOL', `protocol must be ${PROTOCOL}`, { got: parsed.protocol });
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (parsed.event_class !== EVENT_CLASS) {
    const d = deny('BAD_EVENT_CLASS', `event_class must be ${EVENT_CLASS}`, {
      got: parsed.event_class,
    });
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (parsed.claim_ceiling !== CLAIM_CEILING) {
    const d = deny('BAD_CLAIM_CEILING', `claim_ceiling must be ${CLAIM_CEILING}`, {
      got: parsed.claim_ceiling,
    });
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  if (!Object.prototype.hasOwnProperty.call(parsed, 'interaction_id')) {
    const d = deny('INTERACTION_ID_REQUIRED', 'interaction_id required');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (typeof parsed.interaction_id !== 'string' || !INTERACTION_ID_RE.test(parsed.interaction_id)) {
    const d = deny('BAD_INTERACTION_ID', 'interaction_id format invalid');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  if (!Object.prototype.hasOwnProperty.call(parsed, 'content')) {
    const d = deny('CONTENT_REQUIRED', 'content required');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (typeof parsed.content !== 'string') {
    const d = deny('CONTENT_REQUIRED', 'content must be a string');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (parsed.content.length === 0) {
    const d = deny('CONTENT_EMPTY', 'content must be non-empty');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }
  if (parsed.content.length > MAX_CONTENT_CHARS) {
    const d = deny('CONTENT_TOO_LARGE', `content exceeds ${MAX_CONTENT_CHARS} chars`, {
      chars: parsed.content.length,
    });
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  if (CLAIM_PROMOTION_RE.test(parsed.content)) {
    const d = deny('CLAIM_PROMOTION_ATTEMPT', 'content attempts claim promotion / final truth');
    if (ledger) ledger.append('DENIED', d);
    return d;
  }

  if (ledger && ledger.has(parsed.interaction_id)) {
    const dup = {
      status: 'DUPLICATE',
      interaction_id: parsed.interaction_id,
      claim_ceiling: CLAIM_CEILING,
      epistemic: 'IDEMPOTENT_REPLAY',
      scientific_status: 'RAW_NOT_VALIDATED',
    };
    ledger.append('DUPLICATE', dup);
    return dup;
  }

  const { content: redacted, redactions } = redactContent(parsed.content);
  const receiptId = randomUUID();
  const bodyHash = sha256Hex(buf);
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
    content_redacted: redacted,
    redactions,
    provider: typeof parsed.provider === 'string' ? parsed.provider : null,
    model: typeof parsed.model === 'string' ? parsed.model : null,
    submitted_at: typeof parsed.submitted_at === 'string' ? parsed.submitted_at : null,
    received_at: nowIso(),
    privilege: 'NONE',
    aegis: 'OBSERVATION_ONLY_NO_ESCALATION',
  };

  if (ledger) {
    ledger.mark(parsed.interaction_id, receiptId);
    ledger.append('STAGED_UNTRUSTED', {
      receipt_id: receiptId,
      interaction_id: parsed.interaction_id,
      body_sha256: bodyHash,
      redaction_count: redactions.length,
    });
  }

  return staged;
}

/** F10–F12 policy surface (preserve closed gates; empty F12 register). */
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
      note: 'Fail-closed path exercised by A00-A30 adversarial suite',
    },
    f12: {
      id: 'F12',
      status: 'CLOSED_EMPTY_REGISTER',
      legacy_grant_register: [],
      note: 'Empty register; no invent grants',
    },
  };
}

export function healthPayload(host = '127.0.0.1') {
  const bindHost = host === 'localhost' ? '127.0.0.1' : host;
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
    policy: f10f12PolicySurface(),
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
    ...overrides,
  };
}
