import test from 'node:test';
import assert from 'node:assert/strict';
import { validateNavEvent, NAV_EVENT_SCHEMA_VERSION } from '../../../examples/r21/r21r1/nexus-nav-event.mjs';

const FIX_SHA = 'a'.repeat(64);
const ATOM_REF = { asset_id: 'osm-germany-extract-2026-10', atom_sha256: 'b'.repeat(64) };

function event(extra = {}, node = { node_id: 'astra-nav-www-node', capability_class: 'SOFTWARE_ONLY' }) {
  return {
    schema_version: NAV_EVENT_SCHEMA_VERSION,
    claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    event_id: 'map-view-2026-10-10-001',
    event_kind: 'MAP_VIEW',
    source_utc: '2026-10-10T12:00:00Z',
    node,
    location_evidence_class: 'MAP_CAMERA_ONLY',
    privacy_class: 'DEVICE_LOCAL_PRIVATE',
    map_pack_revision: 'vector-2026.10.10-r0',
    ...extra
  };
}

test('a software-only MAP_VIEW event validates', () => {
  assert.equal(validateNavEvent(event()).event_kind, 'MAP_VIEW');
});

test('a SOFTWARE_ONLY node can never claim a hardware GNSS fix', () => {
  assert.throws(
    () => validateNavEvent(event({
      event_kind: 'POSITION_OBSERVED',
      location_evidence_class: 'NAV_FIX_V1',
      nav_fix_ref: { fix_sha256: FIX_SHA }
    })),
    /GNSS_FIX_REQUIRES_HARDWARE_BOUND_NODE/
  );
});

test('a GNSS_HARDWARE_BOUND node may reference a validated fix', () => {
  const e = event(
    { event_kind: 'POSITION_OBSERVED', location_evidence_class: 'NAV_FIX_V1', nav_fix_ref: { fix_sha256: FIX_SHA } },
    { node_id: 'astra-nav-android-node', capability_class: 'GNSS_HARDWARE_BOUND' }
  );
  assert.equal(validateNavEvent(e).location_evidence_class, 'NAV_FIX_V1');
});

test('NAV_FIX_V1 evidence without a fix reference is rejected', () => {
  assert.throws(
    () => validateNavEvent(event({
      event_kind: 'POSITION_OBSERVED',
      location_evidence_class: 'NAV_FIX_V1'
    })),
    /NAV_FIX_REFERENCE_REQUIRED/
  );
});

test('POSITION_OBSERVED without location evidence is rejected', () => {
  assert.throws(
    () => validateNavEvent(event({ event_kind: 'POSITION_OBSERVED', location_evidence_class: 'NONE' })),
    /POSITION_EVENT_REQUIRES_EVIDENCE/
  );
});

test('MAP_VIEW without a pack revision is rejected', () => {
  assert.throws(
    () => validateNavEvent(event({ map_pack_revision: undefined })),
    /MAP_VIEW_REQUIRES_PACK_REVISION/
  );
});

test('ROUTE_COMPUTED requires the pack revision it was computed from', () => {
  assert.throws(
    () => validateNavEvent(event({ event_kind: 'ROUTE_COMPUTED', map_pack_revision: undefined })),
    /ROUTE_COMPUTED_REQUIRES_PACK_REVISION/
  );
  const ok = event({ event_kind: 'ROUTE_COMPUTED', map_pack_revision: 'routing-2026.10.10-r0' });
  assert.equal(validateNavEvent(ok).event_kind, 'ROUTE_COMPUTED');
});

test('PACK_PUBLISHED requires a provenance atom reference', () => {
  assert.throws(
    () => validateNavEvent(event({ event_kind: 'PACK_PUBLISHED', map_pack_revision: undefined })),
    /PACK_PUBLISHED_REQUIRES_ATOM/
  );
});

test('PACK_PUBLISHED requires an OFFLINE_PACK_PRODUCER node', () => {
  assert.throws(
    () => validateNavEvent(event({
      event_kind: 'PACK_PUBLISHED',
      map_pack_revision: undefined,
      provenance_atom_ref: ATOM_REF
    })),
    /PACK_PUBLISHED_REQUIRES_PRODUCER_CAPABILITY/
  );
});

test('a producer node may publish a pack with an atom reference', () => {
  const e = event(
    { event_kind: 'PACK_PUBLISHED', map_pack_revision: undefined, provenance_atom_ref: ATOM_REF },
    { node_id: 'offline-pack-producer-node', capability_class: 'OFFLINE_PACK_PRODUCER' }
  );
  assert.equal(validateNavEvent(e).event_kind, 'PACK_PUBLISHED');
});

test('a nav fix reference on a camera-only event is rejected', () => {
  assert.throws(
    () => validateNavEvent(event({ nav_fix_ref: { fix_sha256: FIX_SHA } })),
    /BAD_NAV_FIX_REFERENCE/
  );
});

test('atom references on non-publish events are rejected', () => {
  assert.throws(
    () => validateNavEvent(event({ provenance_atom_ref: ATOM_REF })),
    /BAD_ATOM_REFERENCE/
  );
});

test('malformed receipts are rejected', () => {
  assert.throws(
    () => validateNavEvent(event({ receipt: { receipt_id: 'short', receipt_sha256: FIX_SHA } })),
    /BAD_RECEIPT/
  );
  const ok = event({ receipt: { receipt_id: 'receipt-2026-10-10-0001', receipt_sha256: FIX_SHA } });
  assert.equal(validateNavEvent(ok).receipt.receipt_id, 'receipt-2026-10-10-0001');
});

test('nexus-link promotion inside an event is rejected', () => {
  assert.throws(() => validateNavEvent(event({ nexus_link_verified: true })), /INVALID_EVENT_CONTRACT/);
});

test('unknown capability classes (no elite births) are rejected', () => {
  assert.throws(
    () => validateNavEvent(event({}, { node_id: 'phantom-node', capability_class: 'ELITE_NODE' })),
    /BAD_NODE_CAPABILITY/
  );
});

test('unknown event kinds are rejected', () => {
  assert.throws(() => validateNavEvent(event({ event_kind: 'ELITE_NODE_BIRTH' })), /BAD_EVENT_KIND/);
});

test('non-device-local privacy classes are rejected', () => {
  assert.throws(() => validateNavEvent(event({ privacy_class: 'CLOUD_SYNCED' })), /PRIVACY_VIOLATION/);
});

test('malformed event ids are rejected', () => {
  assert.throws(() => validateNavEvent(event({ event_id: 'MAP VIEW 1' })), /BAD_EVENT_ID/);
});

test('malformed source timestamps are rejected', () => {
  assert.throws(() => validateNavEvent(event({ source_utc: 'heute mittag' })), /BAD_SOURCE_UTC/);
});
