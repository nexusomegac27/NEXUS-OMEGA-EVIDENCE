/**
 * ORBIS R19 additive public directory reference.
 * NOT wired into the production site. Cursor must bind site-specific globe,
 * build/manifest delivery, permissions, and independent browser readback.
 * No calls to CelesTrak/NOAA per visitor: only same-origin snapshot.
 */
export const MANIFEST_PATH = '/orbis/satellites/satellites.json';
export const DETAIL_PATH = '/orbis/satellites/';
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const NORAD = /^[0-9]{1,9}$/;
const SHA = /^[a-f0-9]{64}$/;
function invariant(ok, message) {
  if (!ok) throw new Error('ORBIS_MANIFEST_INVALID: ' + message);
}
function utc(t) {
  return typeof t === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(t)
    && !Number.isNaN(Date.parse(t));
}
function https(u) {
  try { return new URL(u).protocol === 'https:'; } catch { return false; }
}
/** Boundary validation. Authoritative JSON Schema must ALSO run in the build. */
export function validatePublicManifest(input) {
  invariant(input && typeof input === 'object' && !Array.isArray(input), 'root');
  invariant(input.schema_version === 'nexus-orbis-satellites/1', 'schema_version');
  invariant(input.claim_ceiling === 'C1_DESCRIPTIVE_ONLY', 'ceiling');
  invariant(input.nexus_link_verified === false, 'no_nexus_link_claim');
  invariant(utc(input.generated_utc), 'generated_utc');
  invariant(typeof input.slot_ledger_revision === 'string' && input.slot_ledger_revision.length, 'ledger_revision');
  invariant(Array.isArray(input.satellites) && input.satellites.length <= 20000, 'satellite_array');
  const slugs = new Set(), catnrs = new Set();
  for (const s of input.satellites) {
    invariant(s && typeof s === 'object', 'satellite_object');
    invariant(typeof s.id === 'string' && SLUG.test(s.id) && s.id.length <= 96, 'satellite_slug');
    invariant(typeof s.name === 'string' && s.name.trim().length && s.name.length <= 160, 'satellite_name');
    invariant(typeof s.norad_cat_id === 'string' && NORAD.test(s.norad_cat_id), 'norad_string');
    invariant(!slugs.has(s.id) && !catnrs.has(s.norad_cat_id), 'duplicate_slot');
    slugs.add(s.id); catnrs.add(s.norad_cat_id);
    invariant(s.admission === 'ADMITTED_C1', 'admission');
    invariant(https(s.identity_source_url), 'identity_source');
    invariant(s.orbital_elements === null || (s.orbital_elements &&
      s.orbital_elements.data_class === 'ORBIT_ELEMENTS_EXTERNAL' &&
      SHA.test(s.orbital_elements.sha256) && utc(s.orbital_elements.epoch_utc) &&
      utc(s.orbital_elements.fetched_utc) && https(s.orbital_elements.source_url)), 'orbital_elements');
    invariant(s.position === null || (s.position &&
      s.orbital_elements !== null &&
      s.position.data_class === 'ORBIT_PREDICTED' &&
      Number.isFinite(s.position.lat_deg) && Math.abs(s.position.lat_deg) <= 90 &&
      Number.isFinite(s.position.lng_deg) && Math.abs(s.position.lng_deg) <= 180 &&
      Number.isFinite(s.position.alt_km) && s.position.alt_km >= 0 &&
      utc(s.position.element_epoch_utc) && utc(s.position.target_utc) &&
      utc(s.position.calculated_utc) &&
      s.position.element_epoch_utc === s.orbital_elements.epoch_utc &&
      s.position.source_sha256 === s.orbital_elements.sha256 &&
      typeof s.position.model === 'string' && s.position.model.length > 0), 'predicted_position');
    invariant(Array.isArray(s.observations), 'observation_array');
    for (const o of s.observations) {
      invariant(o && o.data_class === 'LIVE_MEASURED_EXTERNAL' &&
        o.source_norad_cat_id === s.norad_cat_id &&
        typeof o.instrument_id === 'string' && o.instrument_id.length &&
        typeof o.quality_flag === 'string' && o.quality_flag.length &&
        Number.isFinite(o.value) && https(o.source_url) &&
        utc(o.observed_utc) && utc(o.fetched_utc), 'instrument_source_mismatch_or_bad_observation');
    }
  }
  return input;
}
export function detailHref(id) {
  if (typeof id !== 'string' || !SLUG.test(id) || id.length > 96)
    throw new Error('INVALID_SATELLITE_ID');
  return DETAIL_PATH + '?id=' + encodeURIComponent(id);
}
/** Never infer position from NORAD ID, GOES longitude, or a legacy fixture. */
export function selectPlottableSatellites(manifest) {
  validatePublicManifest(manifest);
  return manifest.satellites.filter(s => s.position !== null && s.stale !== true);
}
export function selectDetail(manifest, search) {
  validatePublicManifest(manifest);
  const id = new URLSearchParams(search).get('id');
  if (!id || !SLUG.test(id)) return null;
  return manifest.satellites.find(s => s.id === id) || null;
}
export async function fetchPublicManifest(fetcher = fetch, path = MANIFEST_PATH) {
  invariant(path === MANIFEST_PATH, 'same_origin_only');
  const response = await fetcher(path, { cache: 'no-store', headers: { Accept: 'application/json' } });
  invariant(response && response.ok, 'http_fetch_failed');
  return validatePublicManifest(await response.json());
}
function tag(doc, name, content) {
  const el = doc.createElement(name);
  el.textContent = content;
  return el;
}
function externalLink(doc, label, url) {
  const a = tag(doc, 'a', label);
  a.href = url;
  a.rel = 'noopener noreferrer';
  a.target = '_blank';
  return a;
}
/**
 * Additive list + callback for existing Globe renderer. Do NOT remove existing
 * Canvas2D doctrine markers. Only position-verified entries trigger markers.
 */
export function renderPublicDirectory(mount, manifest, onMarker = () => {}) {
  validatePublicManifest(manifest);
  const doc = mount.ownerDocument;
  const wrap = doc.createElement('section');
  wrap.append(tag(doc, 'h2', 'ORBIS — Quellengebundene Satelliten'));
  wrap.append(tag(doc, 'p', 'Katalogeinträge sind keine direkten NEXUS-Satellitenverbindungen. Positionen werden nur mit geprüftem SGP4-Nachweis gezeigt.'));
  if (!manifest.satellites.length) wrap.append(tag(doc, 'p', 'Noch keine Satelliten im öffentlich freigegebenen Slot Ledger.'));
  const list = doc.createElement('ul');
  for (const s of manifest.satellites) {
    const li = doc.createElement('li');
    const a = tag(doc, 'a', s.name + ' — NORAD ' + s.norad_cat_id);
    a.href = detailHref(s.id);
    li.append(a, tag(doc, 'span', s.position === null ? ' · Position nicht belegt' :
      (s.stale === true ? ' · Positionsdaten veraltet' : ' · Modellposition')));
    list.append(li);
  }
  wrap.append(list);
  mount.replaceChildren(wrap);
  for (const s of selectPlottableSatellites(manifest)) onMarker({
    id: s.id, label: s.name,
    latitude: s.position.lat_deg, longitude: s.position.lng_deg,
    href: detailHref(s.id), data_class: 'ORBIT_PREDICTED',
    target_utc: s.position.target_utc,
    model: s.position.model, source_sha256: s.position.source_sha256
  });
  return manifest.satellites.length;
}
export function renderSelectedDetail(mount, manifest, search) {
  const s = selectDetail(manifest, search);
  const doc = mount.ownerDocument;
  if (!s) {
    mount.replaceChildren(tag(doc, 'p', 'Satellit nicht gefunden oder keine ID ausgewählt.'));
    return false;
  }
  const section = doc.createElement('section');
  section.append(tag(doc, 'h2', s.name + ' · NORAD ' + s.norad_cat_id));
  section.append(tag(doc, 'p', 'C1_DESCRIPTIVE_ONLY · NEXUS_LINK_VERIFIED=0'));
  section.append(externalLink(doc, 'Identitätsquelle', s.identity_source_url));
  if (s.orbital_elements) {
    section.append(tag(doc, 'p', 'Element-Epoche (T1): ' + s.orbital_elements.epoch_utc));
    section.append(tag(doc, 'p', 'Element-Abruf (T2): ' + s.orbital_elements.fetched_utc));
    section.append(externalLink(doc, 'Quelle der Orbitalelemente', s.orbital_elements.source_url));
  } else section.append(tag(doc, 'p', 'Orbitalelemente derzeit nicht belegt.'));
  if (s.position && s.stale !== true)
    section.append(tag(doc, 'p', 'ORBIT_PREDICTED · ' + s.position.model + ' · Zielzeit ' + s.position.target_utc));
  else section.append(tag(doc, 'p', 'Keine aktuelle berechnete Position verfügbar.'));
  if (!s.observations.length) section.append(tag(doc, 'p', 'Keine satellitenspezifischen Instrumentenmesswerte nachgewiesen.'));
  for (const o of s.observations) {
    section.append(tag(doc, 'p', 'LIVE_MEASURED_EXTERNAL · ' + o.metric + ': ' +
      String(o.value) + ' ' + o.unit + ' · Quelle: ' + o.instrument_id +
      ' · Zeit ' + o.observed_utc + ' · Qualitätscode ' + o.quality_flag));
    section.append(externalLink(doc, 'Messdaten-Primärquelle', o.source_url));
  }
  mount.replaceChildren(section);
  return true;
}
