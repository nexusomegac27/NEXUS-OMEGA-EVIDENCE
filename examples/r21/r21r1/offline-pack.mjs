/**
 * NEXUS OMEGA . R21R1 . WP-G3 . nexus-offline-pack/v1 fail-closed pack gate.
 * C1_DESCRIPTIVE_ONLY. Rule: NO_PACK_NO_ROUTE. No pack, no routing claim.
 * GNSS fix evidence is independent of route availability.
 * Every pack binds the R21.1 provenance atom by reference (and inline for ORTHOPHOTO).
 * Schema: schema/r21/r21r1/nexus-offline-pack-v1.schema.json
 */
import { validateProvenanceAtom } from '../nexus-provenance-atom.mjs';

export const OFFLINE_PACK_SCHEMA_VERSION = 'nexus-offline-pack/v1';

const PACK_KINDS = new Set(['VECTOR_MAP', 'DEM', 'ROUTING_GRAPH', 'ORTHOPHOTO']);
const ROLES = new Set(['map_tiles', 'routing_graph', 'dem', 'orthophoto', 'attribution_manifest']);
const ENGINES = new Set(['valhalla', 'brouter', 'graphhopper']);
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const REVISION = /^[a-z0-9]+([._-][a-z0-9]+)*$/;
const SHA = /^[a-f0-9]{64}$/;
const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
const SEMVER = /^\d+\.\d+\.\d+$/;

function isUtc(s) { return typeof s === 'string' && UTC.test(s) && !Number.isNaN(Date.parse(s)); }
function finite(x) { return typeof x === 'number' && Number.isFinite(x); }

export function validateOfflinePack(pack) {
  if (!pack || typeof pack !== 'object' || Array.isArray(pack)) throw new Error('BAD_PACK');
  if (pack.schema_version !== OFFLINE_PACK_SCHEMA_VERSION) throw new Error('INVALID_PACK_CONTRACT');
  if (pack.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY') throw new Error('INVALID_PACK_CONTRACT');
  if (typeof pack.pack_id !== 'string' || !SLUG.test(pack.pack_id)) throw new Error('BAD_PACK_ID');
  if (!PACK_KINDS.has(pack.pack_kind)) throw new Error('BAD_PACK_KIND');
  if (typeof pack.pack_revision !== 'string' || !REVISION.test(pack.pack_revision)) throw new Error('BAD_PACK_REVISION');
  if (!pack.region || typeof pack.region !== 'object' || Array.isArray(pack.region)) throw new Error('BAD_REGION');
  if (typeof pack.region.name !== 'string' || !pack.region.name.trim()) throw new Error('BAD_REGION');
  const bb = pack.region.bbox_wsen;
  if (!Array.isArray(bb) || bb.length !== 4 || !bb.every(finite) ||
      bb[0] >= bb[2] || bb[1] >= bb[3] || bb[0] < -180 || bb[2] > 180 || bb[1] < -90 || bb[3] > 90) throw new Error('BAD_REGION');
  if (!isUtc(pack.produced_utc)) throw new Error('BAD_PRODUCED_UTC');
  if (typeof pack.producer !== 'string' || !pack.producer.trim()) throw new Error('BAD_PRODUCER');
  if (typeof pack.data_license_id !== 'string' || !pack.data_license_id.trim()) throw new Error('BAD_DATA_LICENSE');
  if (!Array.isArray(pack.archives) || pack.archives.length === 0) throw new Error('NO_ARCHIVES');
  const names = new Set();
  for (const a of pack.archives) {
    if (!a || typeof a !== 'object' || Array.isArray(a)) throw new Error('BAD_ARCHIVE');
    if (!ROLES.has(a.role)) throw new Error('BAD_ARCHIVE_ROLE');
    if (typeof a.file_name !== 'string' || !/^[a-z0-9][a-z0-9._-]*$/.test(a.file_name) || names.has(a.file_name)) throw new Error('BAD_ARCHIVE_FILE');
    names.add(a.file_name);
    if (typeof a.sha256 !== 'string' || !SHA.test(a.sha256)) throw new Error('BAD_DIGEST');
    if (!Number.isSafeInteger(a.bytes) || a.bytes < 1) throw new Error('BAD_ARCHIVE_BYTES');
  }
  if (typeof pack.min_client_version !== 'string' || !SEMVER.test(pack.min_client_version)) throw new Error('BAD_MIN_CLIENT_VERSION');
  if (pack.pack_kind === 'ROUTING_GRAPH') {
    const r = pack.routing;
    if (!r || typeof r !== 'object' || Array.isArray(r)) throw new Error('ROUTING_GRAPH_REQUIRES_ENGINE');
    if (!ENGINES.has(r.engine)) throw new Error('BAD_ROUTING_ENGINE');
    if (typeof r.engine_version !== 'string' || !r.engine_version.trim()) throw new Error('BAD_ROUTING_ENGINE');
    if (typeof r.profile !== 'string' || !r.profile.trim()) throw new Error('BAD_ROUTING_ENGINE');
    if (r.companion_pack_revisions !== undefined && !Array.isArray(r.companion_pack_revisions)) throw new Error('BAD_ROUTING_ENGINE');
  } else if (pack.routing !== undefined && pack.routing !== null) {
    throw new Error('ROUTING_ONLY_FOR_ROUTING_GRAPH');
  }
  const ref = pack.provenance_atom_ref;
  if (!ref || typeof ref !== 'object' || Array.isArray(ref) ||
      typeof ref.asset_id !== 'string' || !/^[a-z0-9]+([-_.][a-z0-9]+)*$/.test(ref.asset_id) ||
      typeof ref.atom_sha256 !== 'string' || !SHA.test(ref.atom_sha256)) throw new Error('PROVENANCE_ATOM_REF_REQUIRED');
  if (pack.pack_kind === 'ORTHOPHOTO') {
    try { validateProvenanceAtom(pack.inline_provenance_atom); }
    catch (e) { throw new Error('PROVENANCE_ATOM_REQUIRED'); }
    if (pack.inline_provenance_atom.rights_status !== 'APPROVED_FOR_THIS_USE') throw new Error('DENIED_RIGHTS_NO_PACK');
  } else if (pack.inline_provenance_atom !== undefined && pack.inline_provenance_atom !== null) {
    try { validateProvenanceAtom(pack.inline_provenance_atom); } catch (e) { throw new Error('BAD_INLINE_ATOM'); }
  }
  if (pack.valid_until_utc !== undefined && pack.valid_until_utc !== null && !isUtc(pack.valid_until_utc)) throw new Error('BAD_VALIDITY');
  if (!pack.update_policy || typeof pack.update_policy !== 'object' || Array.isArray(pack.update_policy) ||
      pack.update_policy.rollback_supported !== true) throw new Error('BAD_UPDATE_POLICY');
  if (pack.update_policy.supersedes !== undefined && pack.update_policy.supersedes !== null &&
      (typeof pack.update_policy.supersedes !== 'string' || !SLUG.test(pack.update_policy.supersedes))) throw new Error('BAD_UPDATE_POLICY');
  return pack;
}

/** Fail-closed route availability. No pack, no routing claim; network fallback disguised as offline is impossible by contract. */
export function routeAvailability(pack, request) {
  if (!request || typeof request !== 'object') throw new Error('BAD_REQUEST');
  if (pack === null || pack === undefined) return 'NO_PACK_NO_ROUTE';
  validateOfflinePack(pack);
  if (!isUtc(request.evaluation_utc)) throw new Error('BAD_EVALUATION_TIME');
  if (pack.valid_until_utc && Date.parse(pack.valid_until_utc) < Date.parse(request.evaluation_utc)) return 'PACK_EXPIRED';
  const point = request.point;
  if (!Array.isArray(point) || point.length !== 2 || !point.every(finite)) throw new Error('BAD_POINT');
  const lng = point[0]; const lat = point[1];
  const w = pack.region.bbox_wsen[0]; const s = pack.region.bbox_wsen[1];
  const e = pack.region.bbox_wsen[2]; const n = pack.region.bbox_wsen[3];
  if (lng < w || lng > e || lat < s || lat > n) return 'OUT_OF_COVERAGE';
  if (pack.pack_kind !== 'ROUTING_GRAPH') return 'NO_ROUTING_GRAPH_IN_PACK';
  if (request.requested_pack_revision !== undefined && request.requested_pack_revision !== pack.pack_revision) return 'PACK_REVISION_MISMATCH';
  if (pack.routing.companion_pack_revisions && request.required_companion_revision !== undefined &&
      !pack.routing.companion_pack_revisions.includes(request.required_companion_revision)) return 'PACK_REVISION_MISMATCH';
  return 'ROUTE_AVAILABLE_FROM_PACK';
}
