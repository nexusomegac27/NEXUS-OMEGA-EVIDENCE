/**
 * NEXUS OMEGA . R21.2 . GSD truth gate as a UI reference artifact.
 * C1_DESCRIPTIVE_ONLY. Pure presentation logic: renders nothing, deploys nothing.
 * Consumes the R21 photo-LOD core as a living symbiosis link, not as a copy.
 */
import { selectPhotoLayer, mapMetersPerCssPixel } from './orbis-astra-nav-photo-lod.mjs';

function fmtMeters(m) { return m.toFixed(2).replace('.', ',') + ' m'; }

/** Resolve a truth-bound view state for a zoom level; never fabricates a source. */
export function resolveTruthView(assets, { longitude, latitude, zoom, offline = false }) {
  const requested_mpp = mapMetersPerCssPixel(latitude, zoom);
  const selection = selectPhotoLayer(assets, { longitude, latitude, requested_mpp, offline });
  return Object.assign({}, selection, { zoom, requested_mpp, truth_bar: truthBar(selection) });
}

/** Persistent bottom-right origin bar: "Herkunft: ... | GSD: ... nativ | Lizenz: ..." */
export function truthBar(selection) {
  if (selection.state === 'COVERAGE_GAP') {
    return 'Herkunft: keine lizenzierte Abdeckung | GSD: - | Lizenz: -';
  }
  const gsd = fmtMeters(selection.source_gsd_m);
  const base = 'Herkunft: ' + selection.attribution + ' | GSD: ' + gsd + ' nativ | Lizenz: ' + selection.license_id;
  if (selection.state === 'NATIVE_DETAIL_EXCEEDED') {
    return base + ' | ' + gsd + ' nativ ueberschritten - kein neues Foto-Detail';
  }
  return base + ' | Quellenaufloesung ausreichend';
}
