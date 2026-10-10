/**
 * NEXUS OMEGA . R21.1 . Provenance Atom validator (fail-closed reference).
 * C1_DESCRIPTIVE_ONLY. No runtime, no deploy, no image tiles.
 * Vom Ego zur Herkunft: kein Asset ohne Atom, kein Atom ohne sichtbare Herkunft.
 */
const SHA = /^[a-f0-9]{64}$/;
const ISO = /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}([.][0-9]+)?Z$/;
const RIGHTS = new Set(['RESEARCH_ONLY_UNTIL_CLEARANCE','APPROVED_FOR_THIS_USE','DENIED']);
function finite(x){ return typeof x === 'number' && Number.isFinite(x); }
function nonEmptyString(x){ return typeof x === 'string' && x.trim().length > 0; }
function fmtMeters(m){ return m.toFixed(2).replace('.', ',') + ' m'; }

export function validateProvenanceAtom(atom) {
  if (!atom || typeof atom !== 'object' || Array.isArray(atom)) throw new Error('BAD_ATOM');
  if (!nonEmptyString(atom.asset_id) || !/^[a-z0-9]+([-_.][a-z0-9]+)*$/.test(atom.asset_id)) throw new Error('BAD_ASSET_ID');
  if (!Array.isArray(atom.upstream_contributors) || atom.upstream_contributors.length === 0 ||
      !atom.upstream_contributors.every(nonEmptyString)) throw new Error('BAD_CONTRIBUTORS');
  if (typeof atom.source_url !== 'string' || !atom.source_url.startsWith('https://')) throw new Error('BAD_SOURCE_URL');
  if (!nonEmptyString(atom.license_id)) throw new Error('BAD_LICENSE');
  if (!finite(atom.native_gsd_m) || atom.native_gsd_m <= 0) throw new Error('BAD_GSD');
  if (typeof atom.acquired_utc !== 'string' || !ISO.test(atom.acquired_utc) ||
      !Number.isFinite(Date.parse(atom.acquired_utc))) throw new Error('BAD_CAPTURE_DATE');
  if (typeof atom.asset_sha256 !== 'string' || !SHA.test(atom.asset_sha256)) throw new Error('BAD_DIGEST');
  if (!RIGHTS.has(atom.rights_status)) throw new Error('BAD_RIGHTS_STATE');
  if (!atom.attribution || typeof atom.attribution !== 'object' || Array.isArray(atom.attribution)) throw new Error('BAD_ATTRIBUTION');
  if (atom.attribution.first_class !== true) throw new Error('INVISIBLE_ATTRIBUTION');
  if (!nonEmptyString(atom.attribution.visible_label)) throw new Error('INVISIBLE_ATTRIBUTION');
  if (typeof atom.attribution.expiry_check_required !== 'boolean') throw new Error('BAD_EXPIRY_CHECK');
  if (atom.rights_status === 'RESEARCH_ONLY_UNTIL_CLEARANCE' && atom.attribution.expiry_check_required !== true) throw new Error('BAD_EXPIRY_CHECK');
  if (!nonEmptyString(atom.nexus_transformation)) throw new Error('BAD_TRANSFORMATION');
  if (atom.declared_output_gsd_m !== undefined) {
    if (!finite(atom.declared_output_gsd_m) || atom.declared_output_gsd_m <= 0) throw new Error('BAD_OUTPUT_GSD');
    if (atom.declared_output_gsd_m < atom.native_gsd_m) throw new Error('INVENTED_DETAIL_BEYOND_NATIVE_GSD');
  }
  if (!Array.isArray(atom.symbiose_links) || !atom.symbiose_links.every(nonEmptyString)) throw new Error('BAD_SYMBIOSE_LINKS');
  if (atom.is_living_artifact !== true) throw new Error('NOT_A_LIVING_ARTIFACT');
  return atom;
}

/** Project atom rights onto the R21 photo-LOD rights vocabulary (fail-closed, never approving research-only assets). */
export function lodRightsProjection(atom) {
  validateProvenanceAtom(atom);
  if (atom.rights_status === 'RESEARCH_ONLY_UNTIL_CLEARANCE') return 'PENDING_REVIEW';
  return atom.rights_status;
}

/** Visible origin line: contributors stay as permanent provenance traces, not as owners. */
export function truthLine(atom) {
  validateProvenanceAtom(atom);
  return 'Herkunft: ' + atom.upstream_contributors.join(' | ') +
    ' | GSD: ' + fmtMeters(atom.native_gsd_m) + ' nativ' +
    ' | Lizenz: ' + atom.license_id +
    ' | Rechte: ' + atom.rights_status;
}
