/** NEXUS R15: read-only startup evidence classifier for stalled Cursor nodes. No I/O. */
const STATUSES = new Set(['STARTING_UP','READY','BUSY','DONE','FAILED','STOPPED']);
const CLASS = Object.freeze({
  NO_PROVIDER_RUN: 'NO_PROVIDER_RUN_EVIDENCE',
  INIT_NO_PROGRESS: 'INIT_WITHOUT_PROGRESS_EVIDENCE',
  STATUS_STALE: 'UI_STALE_CANDIDATE',
  DISPATCH_WAIT: 'DISPATCH_WAIT_REPORTED',
  ACTIVE: 'PROGRESS_OBSERVED',
  FINISHED: 'COMPLETE_OR_STOPPED_REPORTED',
  UNKNOWN: 'UNKNOWN_INSUFFICIENT_EVIDENCE'
});
export function classifyStartupEvidence(row) {
  if (!row || typeof row !== 'object' || Array.isArray(row) ||
      typeof row.nodeId !== 'string' || row.nodeId.length < 1 || row.nodeId.length > 200 ||
      !STATUSES.has(row.status)) throw new TypeError('INVALID_NODE_EVIDENCE');
  const hasRun = typeof row.providerRunId === 'string' && row.providerRunId.length > 0;
  const hasProgress = row.progressEvents === true;
  const finished = row.executionFinished === true;
  const awaiting = row.bootstrapComplete === true && row.awaitingDispatch === true;
  let classification = CLASS.UNKNOWN;
  if (row.status === 'STARTING_UP') {
    if (!hasRun) classification = CLASS.NO_PROVIDER_RUN;
    else if (finished || hasProgress) classification = CLASS.STATUS_STALE;
    else if (awaiting) classification = CLASS.DISPATCH_WAIT;
    else classification = CLASS.INIT_NO_PROGRESS;
  } else if (finished || row.status === 'DONE' || row.status === 'STOPPED') classification = CLASS.FINISHED;
  else if (hasRun && hasProgress) classification = CLASS.ACTIVE;
  return Object.freeze({nodeId:row.nodeId, status:row.status, classification,
    rootCause:'NOT_ESTABLISHED', actions:[], restartAuthorized:false, triggerMutationAuthorized:false,
    claimCeiling:'C1_DESCRIPTIVE_ONLY'});
}
export function auditStartupBatch(rows, {maxNodes = 128} = {}) {
  if (!Array.isArray(rows) || !Number.isSafeInteger(maxNodes) || maxNodes < 1 || maxNodes > 1024 || rows.length > maxNodes) throw new RangeError('INVALID_BATCH');
  const seen = new Set(); const classified = [];
  for (const row of rows) {
    const out = classifyStartupEvidence(row);
    if (seen.has(out.nodeId)) throw new TypeError('DUPLICATE_NODE_ID');
    seen.add(out.nodeId); classified.push(out);
  }
  return Object.freeze({observedNodeCount:classified.length, results:Object.freeze(classified),
    claimCeiling:'C1_DESCRIPTIVE_ONLY', productionChanges:0});
}
