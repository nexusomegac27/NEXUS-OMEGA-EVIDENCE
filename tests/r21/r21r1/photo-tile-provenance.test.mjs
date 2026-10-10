import test from 'node:test';
import assert from 'node:assert/strict';
import {
  validateTilesetProduction,
  publishingGate,
  zoomTruth,
  selectProductionLayer,
  visibleTruthLine
} from '../../examples/r21/r21r1/photo-tile-provenance.mjs';
import { mapMetersPerCssPixel } from '../../examples/r21/orbis-astra-nav-photo-lod.mjs';

function atom(extra = {}) {
  return {
    asset_id: 'hamburg-dop20-2018-tiles',
    upstream_contributors: ['Freie und Hansestadt Hamburg, LGV'],
    source_url: 'https://geoportal.hamburg.de/orthophotos',
    license_id: 'DL-DE-BY-2.0',
    native_gsd_m: 0.2,
    acquired_utc: '2018-04-30T11:22:00Z',
    asset_sha256: 'c'.repeat(64),
    rights_status: 'APPROVED_FOR_THIS_USE',
    attribution: { first_class: true, visible_label: '(c) Freie und Hansestadt Hamburg, LGV', expiry_check_required: true },
    nexus_transformation: 'keine (synthetische Test-Fixture)',
    symbiose_links: [],
    is_living_artifact: true,
    ...extra
  };
}

function tileset(extra = {}, atomExtra = {}) {
  const a = atom(atomExtra);
  return {
    provenance_atom: a,
    transformation_chain: [
      { step: 'reproject', method: 'EPSG:25832 nach EPSG:3857', output_gsd_m: 0.2 },
      { step: 'tile-encode', method: 'PMTiles-Kachelung 256px', output_gsd_m: 0.2 }
    ],
    declared_tile_gsd_m: 0.2,
    derived: {
      tile_format: 'PMTILES',
      tileset_sha256: 'd'.repeat(64),
      tile_size_px: 256,
      zoom_min: 10,
      zoom_max: 18,
      footprint_wsen: [9.6, 53.3, 10.5, 53.9]
    },
    visible_attribution_label: a.attribution.visible_label,
    ...extra
  };
}

test('a source-bound tileset with truthful GSD chain validates', () => {
  assert.equal(validateTilesetProduction(tileset()).declared_tile_gsd_m, 0.2);
});

test('research-only assets stay NO_PUBLISH until clearance', () => {
  const ts = tileset({}, { rights_status: 'RESEARCH_ONLY_UNTIL_CLEARANCE' });
  assert.equal(publishingGate(ts), 'NO_PUBLISH_RESEARCH_ONLY_UNTIL_CLEARANCE');
});

test('cleared assets pass the publishing gate', () => {
  assert.equal(publishingGate(tileset()), 'PUBLISH_ALLOWED');
});

test('denied rights are a hard NO_PUBLISH', () => {
  assert.throws(() => validateTilesetProduction(tileset({}, { rights_status: 'DENIED' })), /DENIED_RIGHTS_NO_PUBLISH/);
});

test('invented detail beyond native GSD is rejected', () => {
  const invented = tileset({
    transformation_chain: [
      { step: 'super-resolution', method: 'halluzinierte 4x-Schaerfung', output_gsd_m: 0.05 }
    ],
    declared_tile_gsd_m: 0.05
  });
  assert.throws(() => validateTilesetProduction(invented), /INVENTED_DETAIL_BEYOND_NATIVE_GSD/);
});

test('declared tile GSD must match the transformation chain output', () => {
  const mismatch = tileset({
    transformation_chain: [
      { step: 'reproject', method: 'EPSG:25832 nach EPSG:3857', output_gsd_m: 0.4 }
    ],
    declared_tile_gsd_m: 0.2
  });
  assert.throws(() => validateTilesetProduction(mismatch), /DECLARED_GSD_MISMATCH/);
});

test('DOP20 20cm native GSD is exhausted around zoom 19 in Hamburg', () => {
  const z19 = zoomTruth(tileset(), { latitude: 53.55, zoom: 19 });
  assert.equal(z19.state, 'NATIVE_DETAIL_EXCEEDED');
  assert.equal(z19.new_photographic_detail, false);
  assert.ok(z19.requested_mpp > 0.17 && z19.requested_mpp < 0.19);
});

test('zoom 18 stays within native DOP20 resolution', () => {
  const z18 = zoomTruth(tileset(), { latitude: 53.55, zoom: 18 });
  assert.equal(z18.state, 'NATIVE_RESOLUTION_SUPPORTED');
  assert.ok(z18.requested_mpp > 0.2);
});

test('visible attribution must match the atom label exactly', () => {
  assert.throws(() => validateTilesetProduction(tileset({ visible_attribution_label: 'andere Quelle' })), /ATTRIBUTION_MISMATCH/);
});

test('the production layer selection reuses the R21 photo-LOD core', () => {
  const r = selectProductionLayer(tileset(), { longitude: 10.0037, latitude: 53.5511, zoom: 15, offline: true });
  assert.equal(r.state, 'NATIVE_RESOLUTION_SUPPORTED');
  assert.equal(r.asset_id, 'hamburg-dop20-2018-tiles');
  assert.equal(r.attribution, '(c) Freie und Hansestadt Hamburg, LGV');
});

test('research-only assets produce a coverage gap, never a tile display', () => {
  const r = selectProductionLayer(
    tileset({}, { rights_status: 'RESEARCH_ONLY_UNTIL_CLEARANCE' }),
    { longitude: 10.0037, latitude: 53.5511, zoom: 15 }
  );
  assert.equal(r.state, 'COVERAGE_GAP');
  assert.equal(r.asset_id, null);
});

test('the visible truth line carries contributors, license and tile digest', () => {
  const line = visibleTruthLine(tileset());
  assert.ok(line.startsWith('Herkunft:'));
  assert.ok(line.includes('DL-DE-BY-2.0'));
  assert.ok(line.includes('PMTILES'));
  assert.ok(line.includes('sha256=dddddddddddd'));
});

test('unsupported tile formats are rejected', () => {
  assert.throws(() => validateTilesetProduction(tileset({
    derived: { tile_format: 'JPG', tileset_sha256: 'd'.repeat(64), tile_size_px: 256, zoom_min: 10, zoom_max: 18, footprint_wsen: [9.6, 53.3, 10.5, 53.9] }
  })), /BAD_DERIVED_TILES/);
});

test('unsupported tile sizes are rejected', () => {
  assert.throws(() => validateTilesetProduction(tileset({
    derived: { tile_format: 'PMTILES', tileset_sha256: 'd'.repeat(64), tile_size_px: 333, zoom_min: 10, zoom_max: 18, footprint_wsen: [9.6, 53.3, 10.5, 53.9] }
  })), /BAD_DERIVED_TILES/);
});

test('empty transformation chains are rejected', () => {
  assert.throws(() => validateTilesetProduction(tileset({ transformation_chain: [] })), /BAD_TRANSFORMATION_CHAIN/);
});

test('a bad tileset digest is rejected', () => {
  assert.throws(() => validateTilesetProduction(tileset({
    derived: { tile_format: 'PMTILES', tileset_sha256: 'kurz', tile_size_px: 256, zoom_min: 10, zoom_max: 18, footprint_wsen: [9.6, 53.3, 10.5, 53.9] }
  })), /BAD_DERIVED_TILES/);
});
