/**
 * NEXUS OMEGA . R21R1 . WP-G6 . nexus-nav-event/v1 node symbiosis event contract.
 * C1_DESCRIPTIVE_ONLY. Synthetic producer/consumer reference only.
 * A SOFTWARE_ONLY node can never claim a hardware GNSS fix.
 * No HOMEOSTASIS life receipts are altered; no Elite Node births are implied.
 * Schema: schema/r21/r21r1/nexus-nav-event-v1.schema.json
 */

export const NAV_EVENT_SCHEMA_VERSION = 'nexus-nav-event/v1';

const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SHA = /^[a-f0-9]{64}$/;
const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/;
const CAPABILITY = new Set(['SOFTWARE_ONLY', 'GNSS_HARDWARE_BOUND', 'OFFLINE_PACK_PRODUCER']);
const KINDS = new Set(['POSITION_OBSERVED', 'MAP_VIEW', 'ROUTE_COMPUTED', 'PACK_PUBLISHED']);
const EVIDENCE = new Set(['NONE', 'MAP_CAMERA_ONLY', 'NAV_FIX_V1']);

function isUtc(s) { return typeof s === 'string' && UTC.test(s) && !Number.isNaN(Date.parse(s)); }

export function validateNavEvent(event) {
  if (!event || typeof event !== 'object' || Array.isArray(event)) throw new Error('BAD_EVENT');
  if (event.schema_version !== NAV_EVENT_SCHEMA_VERSION) throw new Error('INVALID_EVENT_CONTRACT');
  if (event.claim_ceiling !== 'C1_DESCRIPTIVE_ONLY') throw new Error('INVALID_EVENT_CONTRACT');
  if (event.nexus_link_verified !== undefined && event.nexus_link_verified !== false) throw new Error('INVALID_EVENT_CONTRACT');
  if (typeof event.event_id !== 'string' || !SLUG.test(event.event_id)) throw new Error('BAD_EVENT_ID');
  if (!KINDS.has(event.event_kind)) throw new Error('BAD_EVENT_KIND');
  if (!isUtc(event.source_utc)) throw new Error('BAD_SOURCE_UTC');
  if (!event.node || typeof event.node !== 'object' || Array.isArray(event.node)) throw new Error('BAD_NODE');
  if (typeof event.node.node_id !== 'string' || !SLUG.test(event.node.node_id)) throw new Error('BAD_NODE');
  if (!CAPABILITY.has(event.node.capability_class)) throw new Error('BAD_NODE_CAPABILITY');
  if (!EVIDENCE.has(event.location_evidence_class)) throw new Error('BAD_LOCATION_EVIDENCE');
  if (event.privacy_class !== 'DEVICE_LOCAL_PRIVATE') throw new Error('PRIVACY_VIOLATION_DEVICE_LOCAL_REQUIRED');
  if (event.location_evidence_class === 'NAV_FIX_V1') {
    if (!event.nav_fix_ref || typeof event.nav_fix_ref !== 'object' || Array.isArray(event.nav_fix_ref) ||
        typeof event.nav_fix_ref.fix_sha256 !== 'string' || !SHA.test(event.nav_fix_ref.fix_sha256)) throw new Error('NAV_FIX_REFERENCE_REQUIRED');
    if (event.node.capability_class !== 'GNSS_HARDWARE_BOUND') throw new Error('GNSS_FIX_REQUIRES_HARDWARE_BOUND_NODE');
  } else if (event.nav_fix_ref !== undefined && event.nav_fix_ref !== null) {
    throw new Error('BAD_NAV_FIX_REFERENCE');
  }
  if (event.event_kind === 'POSITION_OBSERVED' && event.location_evidence_class === 'NONE') throw new Error('POSITION_EVENT_REQUIRES_EVIDENCE');
  if (event.event_kind === 'MAP_VIEW' && event.map_pack_revision === undefined) throw new Error('MAP_VIEW_REQUIRES_PACK_REVISION');
  if (event.event_kind === 'ROUTE_COMPUTED') {
    if (typeof event.map_pack_revision !== 'string' || !event.map_pack_revision.trim()) throw new Error('ROUTE_COMPUTED_REQUIRES_PACK_REVISION');
  }
  if (event.event_kind === 'PACK_PUBLISHED') {
    const ref = event.provenance_atom_ref;
    if (!ref || typeof ref !== 'object' || Array.isArray(ref) ||
        typeof ref.asset_id !== 'string' || !ref.asset_id.trim() ||
        typeof ref.atom_sha256 !== 'string' || !SHA.test(ref.atom_sha256)) throw new Error('PACK_PUBLISHED_REQUIRES_ATOM');
    if (event.node.capability_class !== 'OFFLINE_PACK_PRODUCER') throw new Error('PACK_PUBLISHED_REQUIRES_PRODUCER_CAPABILITY');
  } else if (event.provenance_atom_ref !== undefined && event.provenance_atom_ref !== null) {
    throw new Error('BAD_ATOM_REFERENCE');
  }
  if (event.receipt !== undefined && event.receipt !== null) {
    if (typeof event.receipt !== 'object' || Array.isArray(event.receipt) ||
        typeof event.receipt.receipt_id !== 'string' || event.receipt.receipt_id.length < 8 ||
        typeof event.receipt.receipt_sha256 !== 'string' || !SHA.test(event.receipt.receipt_sha256)) throw new Error('BAD_RECEIPT');
  }
  return event;
}
