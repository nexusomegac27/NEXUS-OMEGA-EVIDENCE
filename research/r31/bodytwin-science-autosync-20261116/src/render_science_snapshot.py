#!/usr/bin/env python3
"""R31 BodyTwin C1 science view -- deterministic OFFLINE candidate renderer.

Consumes only an explicitly curated PUBLIC-safe science source census.
No network, no trust discovery, no GitHub merge, no Hostinger, no sensors,
no real signing, no claim promotion. Output is *not* a publication witness.
One approved deployer must separately authenticate release and witness WWW.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

SCHEMA = "nexus-bodytwin-science-release-candidate/1"
RELEASE = "BT-SCIENCE-C1-20261116-R0"
CEILING = "C1_DESCRIPTIVE_ONLY"
ALLOWED = {
    "HISTORICAL_PUBLIC_VIEWER","RESEARCH_SOURCE_AUDIT_C1",
    "REFERENCE_TEST_ONLY","ARCHITECTURE_RESEARCH_ONLY",
    "LOCAL_ASSET_REPORT_WITH_GAPS","RESEARCH_PROGRAM_C1",
    "RESEARCH_SOURCE_FOUNDATION_C1",
    "PHYSICAL_CAPTURE_PRODUCER_REPORTED_NOT_SECOND_PARTY",
    "SCIENTIFIC_PUBLICATION_INFRASTRUCTURE_C1"
}
HEX40 = re.compile(r"[0-9a-f]{40}")
EVENT_ID = re.compile(r"BT-SCI-20\d\d\d\d\d\d-[A-Z0-9-]+")
ISO_DATE = re.compile(r"20\d\d-\d\d-\d\d")
PRIVATE_MARKERS = ("sk-proj-", "ghp_", "github_pat_", "private_key", "api_token",
                   "raw_imu", "patient_record", "patient_name", "consent_granted")

class ContractError(ValueError):
    pass

def uniq(pairs):
    out = {}
    for key, val in pairs:
        if key in out:
            raise ContractError("DUPLICATE_FIELD")
        out[key] = val
    return out

def _bad_const(v):
    raise ContractError("NONFINITE_JSON")

def load_bytes(raw: bytes):
    if len(raw) < 1 or len(raw) > 64000:
        raise ContractError("BAD_INPUT_SIZE")
    try:
        return json.loads(raw.decode("utf-8", "strict"),
                          object_pairs_hook=uniq, parse_constant=_bad_const)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError("MALFORMED_JSON") from exc

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def _date(value):
    if not isinstance(value, str) or not ISO_DATE.fullmatch(value):
        raise ContractError("DATE_FORMAT")
    from datetime import date
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ContractError("DATE_INVALID") from exc

def _source(value):
    if not isinstance(value, str):
        raise ContractError("SOURCE_NOT_STRING")
    prefix = "https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/"
    if value in ("https://www.nexus-mobile.de/bodytwin/",):
        return
    if not value.startswith(prefix):
        raise ContractError("SOURCE_ORIGIN_NOT_ALLOWLISTED")
    tail = value[len(prefix):]
    if re.fullmatch(r"pull/[1-9]\d{0,5}", tail):
        return
    bits = tail.split("/", 3)
    if len(bits) == 4 and bits[0] == "blob" and HEX40.fullmatch(bits[1]):
        if not bits[2] or not bits[3] or ".." in bits[3].split("/"):
            raise ContractError("SOURCE_PATH_BAD")
        return
    raise ContractError("SOURCE_COMMIT_NOT_PINNED")

def validate(doc):
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise ContractError("INVALID_SCHEMA")
    if doc.get("release_id") != RELEASE or doc.get("claim_ceiling") != CEILING:
        raise ContractError("INVALID_RELEASE_OR_CLAIM")
    if doc.get("claim_promotion") is not False or doc.get("publication_status") != "CANDIDATE_NOT_WWW_WITNESSED":
        raise ContractError("CLAIM_OR_WWW_PROMOTION")
    if doc.get("public_safe_metadata_only") is not True or doc.get("auto_execution_authorized") is not False:
        raise ContractError("PUBLICATION_PERMISSION_CLAIM")
    for key, expected in (("bodytwin_validated","NO"),
                          ("consent_bind","OPEN"),("trial_001","DESIGNED_NOT_EXECUTED"),
                          ("whole_body_pose_validated",False),("clinical_validated",False)):
        if doc.get(key) != expected:
            raise ContractError("UNAUTHORIZED_SCIENCE_PROMOTION_"+key)
    events = doc.get("events")
    if not isinstance(events, list) or len(events) < 1 or len(events) > 100:
        raise ContractError("EVENT_COUNT")
    ids, prev = set(), ""
    for e in events:
        if not isinstance(e, dict):
            raise ContractError("BAD_EVENT")
        if set(e) != {"id","date","title","summary","class","evidence","bodytwin_science","source"}:
            raise ContractError("EVENT_FIELDS")
        if not isinstance(e["id"], str) or not EVENT_ID.fullmatch(e["id"]):
            raise ContractError("BAD_EVENT_ID")
        if e["id"] in ids:
            raise ContractError("EVENT_DUPLICATE")
        ids.add(e["id"])
        _date(e["date"])
        if e["date"] < prev:
            raise ContractError("EVENT_ORDER")
        prev = e["date"]
        if e["class"] not in ALLOWED:
            raise ContractError("EVENT_CLASS")
        for key in ("title","summary","evidence"):
            if not isinstance(e[key], str) or len(e[key]) < 4 or len(e[key]) > 850:
                raise ContractError("EVENT_TEXT_"+key)
        if type(e["bodytwin_science"]) is not bool:
            raise ContractError("EVENT_SCIENCE_FLAG")
        _source(e["source"])
        if e["class"] == "PHYSICAL_CAPTURE_PRODUCER_REPORTED_NOT_SECOND_PARTY":
            if "nicht unabhängig" not in e["summary"] or "Live-Sensoranbindung" not in e["summary"]:
                raise ContractError("R21_PHYSICAL_ORIGINAL_GAP_MISSING")
    if not any(e["class"] == "PHYSICAL_CAPTURE_PRODUCER_REPORTED_NOT_SECOND_PARTY" for e in events):
        raise ContractError("MISSING_PHYSICAL_UNCERTAINTY")
    if any(k not in doc.get("open_gates",[]) for k in
            ("BODYTWIN_VALIDATED_NO","PHYSICAL_IMU_TO_BODYTWIN_NOT_ESTABLISHED","CONSENT_BIND_OPEN")):
        raise ContractError("REQUIRED_OPEN_GATES_MISSING")
    raw = json.dumps(doc,ensure_ascii=False,sort_keys=True).lower()
    if any(s in raw for s in PRIVATE_MARKERS):
        raise ContractError("PUBLIC_SENSITIVE_MARKER")
    return doc

def render(doc: dict):
    validate(doc)
    events = doc["events"]
    payload = {
        "schema":"nexus-bodytwin-public-science-candidate/1",
        "object":doc["object"],
        "release_id":doc["release_id"],
        "claim_ceiling":CEILING,
        "claim_promotion":False,
        "publication_status":"CANDIDATE_NOT_WWW_WITNESSED",
        "bodytwin_validated":"NO",
        "consent_bind":"OPEN",
        "trial_001":"DESIGNED_NOT_EXECUTED",
        "source_date":doc["candidate_created_utc"][:10],
        "event_count":len(events),
        "events":events,
        "open_gates":doc["open_gates"],
        "source_ledger_note":"C1 source summary; not a signed publication or independently witnessed deployment."
    }
    payload_bytes=(json.dumps(payload,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8")
    title="BodyTwin – Wissenschaftlicher Stand | NEXUS OMEGA"
    e=html.escape
    items=[]
    for event in events:
        kind=e(event["class"])
        items.append(
            '<li class="event"><time datetime="'+e(event["date"])+'">'+e(event["date"])+'</time>'
            '<div><h2>'+e(event["title"])+'</h2><p>'+e(event["summary"])+'</p>'
            '<small>Belegklasse: '+kind+' · '+e(event["evidence"])+'</small>'
            '<p><a href="'+e(event["source"],quote=True)+'" rel="noopener noreferrer">Quellbeleg öffnen</a></p>'
            '</div></li>'
        )
    page='''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>'''+e(title)+'''</title>
<meta name="description" content="Quellengebundene C1-Forschungsstände zu BodyTwin. Keine medizinische oder Körpervalidierung.">
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{background:#071626;color:#edf4fa;font:16px/1.6 system-ui,sans-serif;margin:0}
main{max-width:1030px;padding:22px;margin:auto}a{color:#9df4dd}a:focus-visible{outline:3px solid #ffd28a;outline-offset:3px}
.status{border:1px solid #4e6a80;border-radius:12px;background:#152c40;padding:16px;margin:20px 0}
.event{display:grid;grid-template-columns:112px 1fr;gap:14px;padding:18px 0;border-top:1px solid #355066}
.event time{font:600 12px/1.8 ui-monospace,monospace;color:#a7d8d2}
h1{line-height:1.2;font-size:clamp(25px,3vw,38px)}h2{font-size:18px;line-height:1.35;margin:0}
small{color:#c4d6e2;overflow-wrap:anywhere}p{overflow-wrap:anywhere;margin:7px 0 12px}
ul{list-style:none;margin:0;padding:0}footer{padding:18px 0;border-top:1px solid #355066}
@media(max-width:600px){.event{grid-template-columns:1fr;gap:2px}main{padding:14px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style></head><body><main>
<nav><a href="/bodytwin/">Zur 4D-Ansicht</a> · <a href="/bodytwin/updates/">Frühere Fortschrittsakte</a> ·
<a href="/bodytwin/science/current.json">Wissenschafts-JSON</a></nav>
<h1>BodyTwin · wissenschaftlicher Forschungsstand</h1>
<p>Quellenstand: <time datetime="'''+e(doc["candidate_created_utc"][:10])+'''">'''+e(doc["candidate_created_utc"][:10])+'''</time>.
Die folgenden Einträge unterscheiden Referenzquellen, technische Tests, Forschungsentwürfe und lediglich berichtete Messungen.</p>
<section class="status" aria-label="Wissenschaftliche Grenzen">
<strong>C1_DESCRIPTIVE_ONLY · BODYTWIN_VALIDATED=NO</strong>
<p>Consent-Bindung OPEN · Trial 001 DESIGNED_NOT_EXECUTED · keine klinische, anatomische oder physikalische Körpervalidierung.</p>
<p>Wichtiger Unterschied: Ein Quellenbericht über einen Sensorlauf beweist keine unabhängige Rohdatenprüfung.
Ein Feed-Takt ist keine neue wissenschaftliche Beobachtung.</p>
</section><section aria-label="Chronologie"><ul>'''+''.join(items)+'''</ul></section>
<footer><p>Diese Seite wurde aus einem datierten C1-Quellregister generiert. Veröffentlichung, Hostinger-Status und unabhängige WWW-Beobachtung sind eigenständig nachzuweisen. Ursprüngliche private Messdaten werden nicht bereitgestellt.</p></footer>
</main></body></html>
'''
    return page.encode("utf-8"),payload_bytes

def main():
    ap=argparse.ArgumentParser(description="render BodyTwin science metadata ONLY to disposable staging")
    ap.add_argument("--input",required=True)
    ap.add_argument("--output-dir",required=True,help="existing disposable staging directory ONLY")
    args=ap.parse_args()
    raw=Path(args.input).read_bytes()
    html_bytes,json_bytes=render(load_bytes(raw))
    out=Path(args.output_dir)
    if not out.is_dir() or out.is_symlink():
        raise ContractError("STAGING_DIR_MUST_EXIST_AND_NOT_BE_SYMLINK")
    for name,data in (("index.html",html_bytes),("current.json",json_bytes)):
        target=out/name
        if target.exists() or target.is_symlink():
            raise ContractError("NO_OVERWRITE_IN_CANDIDATE_GENERATOR")
        with target.open("xb") as fh:
            fh.write(data)
    print(json.dumps({"state":"OFFLINE_C1_CANDIDATE_ONLY","html_bytes":len(html_bytes),
          "html_sha256":digest(html_bytes),"json_bytes":len(json_bytes),
          "json_sha256":digest(json_bytes),"wwwwrite":False},sort_keys=True))
if __name__=="__main__":
    main()
