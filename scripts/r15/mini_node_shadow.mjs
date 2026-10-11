/**
 * NEXUS R15 bounded mini-node observer — C1, observation only.
 * No network, storage, subprocess, worker, approval or dispatch capability.
 * Bio-inspired trend transitions are not entropy, chemotaxis or consensus.
 */
export const STATES = Object.freeze({SEARCHING:'SEARCHING', APPROACHING:'APPROACHING', REORIENTING:'REORIENTING', ERROR:'ERROR'});
const INPUT_FIELDS = new Set(['signal', 'localActiveCount', 'messageId', 'critical']);
const OPTION_FIELDS = new Set(['clock', 'up', 'down', 'enter', 'exit', 'confirmations', 'maxHistory', 'maxDedupe', 'ttlMs']);
const isInt = Number.isSafeInteger;

export function createMiniNodeShadow(options = {}) {
  if (!options || Array.isArray(options) || typeof options !== 'object') throw new TypeError('INVALID_OPTIONS');
  for (const k of Object.keys(options)) if (!OPTION_FIELDS.has(k)) throw new TypeError('UNKNOWN_OPTION');
  const c = {clock: () => Date.now(), up: 0.05, down: 0.10, enter: 3, exit: 1,
    confirmations: 2, maxHistory: 8, maxDedupe: 256, ttlMs: 5000, ...options};
  if (typeof c.clock !== 'function' || !Number.isFinite(c.up) || c.up < 0 || c.up > 1 ||
      !Number.isFinite(c.down) || c.down <= 0 || c.down > 1 ||
      !isInt(c.enter) || c.enter < 1 || !isInt(c.exit) || c.exit < 0 || c.exit >= c.enter ||
      !isInt(c.confirmations) || c.confirmations < 1 || c.confirmations > 20 ||
      !isInt(c.maxHistory) || c.maxHistory < 1 || c.maxHistory > 256 ||
      !isInt(c.maxDedupe) || c.maxDedupe < 1 || c.maxDedupe > 4096 ||
      !isInt(c.ttlMs) || c.ttlMs < 1 || c.ttlMs > 86400000) throw new RangeError('INVALID_LIMITS');
  let state = STATES.SEARCHING, previous = null, streak = 0, recovery = 0;
  let thresholdMet = false, lastTime = -Infinity;
  const history = [], seen = new Map();
  const result = (accepted, reason, at) => Object.freeze({accepted, reason, state, localThresholdMet: thresholdMet,
    at, observationOnly: true, effects: 0, runtimeAuthority: 'NONE', claimCeiling:'C1_DESCRIPTIVE_ONLY'});
  function error(reason, at) { state = STATES.ERROR; streak = 0; recovery = 0; return result(false, reason, at); }
  function step(input) {
    const at = c.clock();
    if (!Number.isSafeInteger(at) || at < 0 || at < lastTime) return error('INVALID_OR_BACKWARDS_CLOCK', at);
    lastTime = at;
    if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).some(k => !INPUT_FIELDS.has(k))) return error('INVALID_ENVELOPE', at);
    if (typeof input.signal !== 'number' || !Number.isFinite(input.signal) || input.signal < 0 || input.signal > 1) return error('INVALID_SIGNAL', at);
    if ('localActiveCount' in input && (!isInt(input.localActiveCount) || input.localActiveCount < 0)) return error('INVALID_LOCAL_COUNT', at);
    if ('critical' in input && typeof input.critical !== 'boolean') return error('INVALID_CRITICAL_FLAG', at);
    if ('messageId' in input && (typeof input.messageId !== 'string' || !/^[a-zA-Z0-9_.:-]{1,200}$/.test(input.messageId))) return error('INVALID_MESSAGE_ID', at);
    for (const [id, until] of seen) if (until <= at) seen.delete(id);
    if (input.messageId !== undefined) {
      if (seen.has(input.messageId)) return result(false, 'DUPLICATE', at);
      if (seen.size >= c.maxDedupe) return error('DEDUPE_CAPACITY', at);
      seen.set(input.messageId, at + c.ttlMs);
    }
    if (input.localActiveCount !== undefined) {
      if (!thresholdMet && input.localActiveCount >= c.enter) thresholdMet = true;
      else if (thresholdMet && input.localActiveCount <= c.exit) thresholdMet = false;
    }
    const delta = previous === null ? 0 : input.signal - previous;
    previous = input.signal;
    history.push(Object.freeze({at, signal: input.signal, state}));
    if (history.length > c.maxHistory) history.shift();
    if (state === STATES.ERROR) {
      recovery++;
      if (recovery < c.confirmations) return result(false, 'RECOVERY_PENDING', at);
      state = STATES.SEARCHING; recovery = 0; streak = 0;
      return result(true, 'RECOVERED', at);
    }
    if (delta >= c.up && (input.critical ?? false)) {
      streak++;
      if (streak < c.confirmations) return result(true, 'CONFIRMATION_PENDING', at);
    } else if (delta < c.up) streak = 0;
    if (delta >= c.up) { state = STATES.APPROACHING; streak = 0; return result(true, 'IMPROVING', at); }
    if (delta <= -c.down) { state = STATES.REORIENTING; streak = 0; return result(true, 'DEGRADING', at); }
    if (state === STATES.REORIENTING) { state = STATES.SEARCHING; return result(true, 'STABILIZED', at); }
    return result(true, 'STABLE', at);
  }
  function snapshot() { return Object.freeze({state, localThresholdMet: thresholdMet, historySize: history.length,
    dedupeSize: seen.size, lastTime, runtimeAuthority:'NONE'}); }
  function spawn() { throw new Error('AUTONOMOUS_REPLICATION_PROHIBITED'); }
  return Object.freeze({step, snapshot, spawn});
}
