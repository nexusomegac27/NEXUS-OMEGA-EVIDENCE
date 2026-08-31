#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from a83_decision import decision_function
from a83_sentinel import sentinel_hits

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ROLES={"OPERATOR","AXIOM","CURSOR_PRAXIS","EXTERNAL_AGENT","VALIDATOR","COPILOT_CONTEXT_CONSUMER"}
ACTOR_ROLES={"PRODUCER","VALIDATOR","IMPLEMENTER","OPERATOR","CONTEXT_CONSUMER"}
OBS={"OBS0_UNOBSERVABLE","OBS1_PROVIDER_AGGREGATE","OBS2_PROVIDER_EVENT","OBS3_MEDIATED_EVENT","OBS4_MUTUAL_RECEIPT"}
RA={"RA0_NONE","RA1_SELF_ASSERTED","RA2_MUTUAL_BYTE_BOUND","RA3_AUTHENTICATED_PLATFORM","RA4_SIGNED_OR_TIMESTAMPED","RA5_EXTERNAL_TRANSPARENCY_WITNESS"}
SR={"SR0_OPERATIONAL","SR1_PROVENANCE_SUPPORT","SR2_PROCESS_EVENT","SR3_CLAIM_EVIDENCE","SR4_GOVERNANCE_VALIDATION","SR5_SECURITY_INTEGRITY"}
TRANSPORT={"CHAT_UI","API","GITHUB","GIT","FILE_UPLOAD","OPERATOR_COPY_PASTE","CONTROLLED_GATEWAY","OTHER"}
REQUIRED={"schema_version","handoff_id","object_id","parent_record_sha256","sender_role","recipient_role","actor_role","claim_ceiling","claim_promotion","integration_authority","observability_class","receipt_assurance","scientific_relevance_class","transport_class","payload_sha256","payload_bytes","sunset_months","auto_execute","network_write","created_at_utc","caveats"}

def ledger_record_hashes(root: Path) -> set[str]:
    p=root/'communication/index/v1/records.jsonl'
    if not p.exists(): return set()
    out=set()
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.strip(): out.add(json.loads(line)['record_sha256'])
    return out

def validate_envelope(env: dict, payload_text: str | None=None, root: Path | None=None) -> list[str]:
    e=[]
    if set(env) != REQUIRED: e.append('A83_SCHEMA_KEYSET')
    if env.get('schema_version')!='1.0.0': e.append('A83_SCHEMA_VERSION')
    if not isinstance(env.get('handoff_id'),str) or len(env['handoff_id'])<8: e.append('A83_HANDOFF_ID')
    if not SHA256_RE.fullmatch(str(env.get('parent_record_sha256',''))): e.append('A83_PARENT_SHA256')
    if env.get('sender_role') not in ROLES or env.get('recipient_role') not in ROLES: e.append('A83_ROLE_INVALID')
    if env.get('actor_role') not in ACTOR_ROLES: e.append('A83_ACTOR_ROLE_INVALID')
    if env.get('claim_ceiling')!='C1': e.append('A83_CLAIM_CEILING')
    if env.get('claim_promotion') is not False: e.append('A83_CLAIM_PROMOTION')
    if env.get('integration_authority')!='NONE': e.append('A83_INTEGRATION_AUTHORITY')
    if env.get('observability_class') not in OBS: e.append('A83_OBSERVABILITY')
    if env.get('receipt_assurance') not in RA: e.append('A83_RECEIPT_ASSURANCE')
    if env.get('scientific_relevance_class') not in SR: e.append('A83_RELEVANCE')
    if env.get('transport_class') not in TRANSPORT: e.append('A83_TRANSPORT')
    if not SHA256_RE.fullmatch(str(env.get('payload_sha256',''))): e.append('A83_PAYLOAD_SHA256')
    if not isinstance(env.get('payload_bytes'),int) or env.get('payload_bytes',-1)<0: e.append('A83_PAYLOAD_BYTES')
    if not isinstance(env.get('sunset_months'),int) or env.get('sunset_months',0)<12: e.append('A83_SUNSET_LT_12_MONTHS')
    if env.get('auto_execute') is not False: e.append('A83_AUTO_EXECUTE_PROHIBITED')
    if env.get('network_write') is not False: e.append('A83_NETWORK_WRITE_PROHIBITED')
    if env.get('sender_role')==env.get('recipient_role') and env.get('actor_role')=='VALIDATOR': e.append('A83_IDENTITY_FUSION')
    if env.get('observability_class')=='OBS0_UNOBSERVABLE' and env.get('receipt_assurance') in {'RA3_AUTHENTICATED_PLATFORM','RA4_SIGNED_OR_TIMESTAMPED','RA5_EXTERNAL_TRANSPARENCY_WITNESS'}:
        e.append('A83_ASSURANCE_OBSERVABILITY_CONFLICT')
    if root is not None and SHA256_RE.fullmatch(str(env.get('parent_record_sha256',''))):
        if env['parent_record_sha256'] not in ledger_record_hashes(root): e.append('A83_PARENT_NOT_IN_LEDGER')
    if payload_text is not None:
        e.extend('A83_SENTINEL_'+x for x in sentinel_hits(payload_text))
    return sorted(set(e))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('envelope',type=Path); ap.add_argument('--payload',type=Path); ap.add_argument('--root',type=Path)
    ns=ap.parse_args(); env=json.loads(ns.envelope.read_text(encoding='utf-8')); payload=ns.payload.read_text(encoding='utf-8') if ns.payload else None
    errs=validate_envelope(env,payload,ns.root); out={'errors':errs,'verdict':decision_function(errs)}; print(json.dumps(out,indent=2,sort_keys=True)); raise SystemExit(1 if errs else 0)
if __name__=='__main__': main()
