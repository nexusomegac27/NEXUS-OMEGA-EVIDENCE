/**
 * NEXUS OMEGA . R21R1 . WP-G4 . Source-to-tile production provenance and GSD gate.
 * C1_DESCRIPTIVE_ONLY. No image bytes shipped; no publish of uncleared photo assets.
 * Reuses the R21.1 provenance atom and the R21 photo-LOD selection core via imports
 * (living symbiosis links, not copied forks).
 */
import { validateProvenanceAtom, lodRightsProjection, truthLine } from '../nexus-provenance-atom.mjs';
import { selectPhotoLayer, mapMetersPerCssPixel } from '../orbis-astra-nav-photo-lod.mjs';

const SHA = /^[a-f0-9]{64}$/;

export function validateTilesetProduction(tileset) {
  if (!tileset || typeof tileset !== 'object' || Array.isArray(tileset)) throw new Error('BAD_TILESET');
  const atom = validateProvenanceAtom(tileset.provenance_atom);
  if (atom.rights_status === 'DENIED') throw new Error('DENIED_RIGHTS_NO_PUBLISH');
  if (!Array.isArray(tileset.transformation_chain) || tileset.transformation_chain.length === 0) throw new Error('BAD_TRANSFORMATION_CHAIN');
  let lastGsd = atom.native_gsd_m;
  for (const step of tileset.transformation_chain) {
    if (!step || typeof step !== 'object' || Array.isArray(step)) throw new Error('BAD_TRANSFORMATION_CHAIN');
    if (typeof step.step !== 'string' || !step.step.trim()) throw new Error('BAD_TRANSFORMATION_CHAIN');
    if (typeof step.method !== 'string' || !step.method.trim()) throw new Error('BAD_TRANSFORMATION_CHAIN');
    if (typeof step.output_gsd_m !== 'number' || !Number.isFinite(step.output_gsd_m) || step.output_gsd_m <= 0) throw new Error('BAD_TRANSFORMATION_CHAIN');
    if (step.output_gsd_m < lastGsd) throw new Error('INVENTED_DETAIL_BEYOND_NATIVE_GSD');
    lastGsd = step.output_gsd_m;
  }
  if (tileset.declared_tile_gsd_m !== lastGsd) throw new Error('DECLARED_GSD_MISMATCH');
  const derived = tileset.derived;
  if (!derived || typeof derived !== 'object' || Array.isArray(derived)) throw new Error('BAD_DERIVED_TILES');
  if (derived.tile_format !== 'PMTILES' && derived.tile_format !== 'COG') throw new Error('BAD_DERIVED_TILES');
  if (typeof derived.tileset_sha256 !== 'string' || !SHA.test(derived.tileset_sha256)) throw new Error('BAD_DERIVED_TILES');
  if (derived.tile_size_px !== 256 && derived.tile_size_px !== 512) throw new Error('BAD_DERIVED_TILES');
  if (!Number.isFinite(derived.zoom_min) || !Number.isFinite(derived.zoom_max) ||
      derived.zoom_min < 0 || derived.zoom_max < derived.zoom_min) throw new Error('BAD_DERIVED_TILES');
  if (!Array.isArray(derived.footprint_wsen) || derived.footprint_wsen.length !== 4 ||
      !derived.footprint_wsen.every(Number.isFinite) ||
      derived.footprint_wsen[0] >= derived.footprint_wsen[2] || derived.footprint_wsen[1] >= derived.footprint_wsen[3]) throw new Error('BAD_DERIVED_TILES');
  if (typeof tileset.visible_attribution_label !== 'string' ||
      tileset.visible_attribution_label !== atom.attribution.visible_label) throw new Error('ATTRIBUTION_MISMATCH');
  return tileset;
}

/** Production gate: RESEARCH_ONLY_UNTIL_CLEARANCE is a hard NO_PUBLISH state. */
export function publishingGate(tileset) {
  validateTilesetProduction(tileset);
  const rights = tileset.provenance_atom.rights_status;
  if (rights === 'DENIED') return 'DENIED_NO_PUBLISH';
  if (lodRightsProjection(tileset.provenance_atom) === 'PENDING_REVIEW') return 'NO_PUBLISH_RESEARCH_ONLY_UNTIL_CLEARANCE';
  return 'PUBLISH_ALLOWED';
}

/** Zoom truth: beyond native GSD the renderer must show NATIVE_DETAIL_EXCEEDED, never new photographic detail. */
export function zoomTruth(tileset, { latitude, zoom }) {
  validateTilesetProduction(tileset);
  const requested_mpp = mapMetersPerCssPixel(latitude, zoom);
  const native = tileset.provenance_atom.native_gsd_m;
  if (requested_mpp < native) {
    return { state: 'NATIVE_DETAIL_EXCEEDED', requested_mpp, native_gsd_m: native, new_photographic_detail: false };
  }
  return { state: 'NATIVE_RESOLUTION_SUPPORTED', requested_mpp, native_gsd_m: native, new_photographic_detail: false };
}

/** Bind the existing R21 photo-LOD core: build the production asset and delegate selection. */
export function selectProductionLayer(tileset, { longitude, latitude, zoom, offline = false }) {
  validateTilesetProduction(tileset);
  const atom = tileset.provenance_atom;
  const approved = atom.rights_status === 'APPROVED_FOR_THIS_USE';
  const asset = {
    id: atom.asset_id,
    kind: 'AERIAL_ORTHOPHOTO',
    native_gsd_m: atom.native_gsd_m,
    bounds_wsen: derivedFootprintCopy(tileset),
    source_url: atom.source_url,
    source_name: atom.upstream_contributors.join(', '),
    license_id: atom.license_id,
    required_attribution: atom.attribution.visible_label,
    acquired_utc: atom.acquired_utc,
    asset_sha256: tileset.derived.tileset_sha256,
    rights_status: approved ? 'APPROVED_FOR_THIS_USE' : 'PENDING_REVIEW',
    offline_available: offline === true && approved
  };
  return selectPhotoLayer([asset], { longitude, latitude, requested_mpp: mapMetersPerCssPixel(latitude, zoom), offline: offline === true });
}

/** Visible provenance line for the permanent attribution bar (Herkunft bleibt sichtbar). */
export function visibleTruthLine(tileset) {
  validateTilesetProduction(tileset);
  return truthLine(tileset.provenance_atom) + ' | Kacheln: ' + tileset.derived.tile_format +
    ' sha256=' + tileset.derived.tileset_sha256.slice(0, 12);
}

function derivedFootprintCopy(tileset) {
  return tileset.derived.footprint_wsen.slice();
}
