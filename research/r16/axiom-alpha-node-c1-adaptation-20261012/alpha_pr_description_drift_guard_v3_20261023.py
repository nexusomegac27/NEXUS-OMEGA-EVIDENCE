#!/usr/bin/env python3
"""C1 research-only guard for stale PR-description inventory assertions.

Accepts a caller-provided GitHub PR metadata snapshot; it does not fetch or
authenticate the snapshot, authorize a write, approve CI, or merge anything.
Only a narrowly specified legacy description grammar is supported. Unsupported
claims fail closed as INCOMPLETE; never infer authorization from CONSISTENT.
"""
import re

SHA40=re.compile(r'^[0-9a-f]{40}$')
WORDS={'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,
       'seven':7,'eight':8,'nine':9,'ten':10}
CLAIM_HEAD=re.compile(r'\bto pinned head ([0-9a-f]{40})\b')
CLAIM_BASE=re.compile(r'\bpinned main ([0-9a-f]{40})\b')
CLAIM_COMMITS=re.compile(r'(?<![\w+.\-])([0-9]+) commits ahead\b')
CLAIM_FILES=re.compile(r'(?<![\w+.\-])([0-9]+|zero|one|two|three|four|five|six|seven|eight|nine|ten) added (Markdown|Python|JSON) files only\b',re.I)
CLAIM_SCOPE=re.compile(r'\bunder (?:the )?existing (research/[a-z0-9_-]+/[a-z0-9_-]+/) lane\b')
EXT={'MARKDOWN':'.md','PYTHON':'.py','JSON':'.json'}


def audit_pr_description(snapshot):
    """Return CONSISTENT, DRIFT, or INCOMPLETE with bounded diagnostics."""
    if not isinstance(snapshot,dict):
        return {'status':'INCOMPLETE','reasons':['snapshot_type']}
    body=snapshot.get('body')
    base=snapshot.get('base_sha')
    head=snapshot.get('head_sha')
    commits=snapshot.get('commits')
    files=snapshot.get('files')
    if (not isinstance(body,str) or not body or len(body)>100000
        or not isinstance(base,str) or not SHA40.fullmatch(base)
        or not isinstance(head,str) or not SHA40.fullmatch(head)
        or type(commits) is not int or commits<0
        or not isinstance(files,list) or len(files)>3000):
        return {'status':'INCOMPLETE','reasons':['invalid_snapshot']}
    if body.count('CLAIM_CEILING=C1_DESCRIPTIVE_ONLY')!=1:
        return {'status':'INCOMPLETE','reasons':['claim_ceiling_missing_or_ambiguous']}
    matches=[r.findall(body) for r in (CLAIM_BASE,CLAIM_HEAD,CLAIM_COMMITS,CLAIM_FILES,CLAIM_SCOPE)]
    if any(len(m)!=1 for m in matches):
        return {'status':'INCOMPLETE','reasons':['unparseable_or_ambiguous_description_claim']}
    claimed_base,claimed_head=matches[0][0],matches[1][0]
    commit_text=matches[2][0]
    count_text,kind=matches[3][0]
    # Explicit ASCII unsigned integer grammar and domain bounds. No exception
    # or ambiguous readiness from Unicode digits, signs, decimals or huge claims.
    if len(commit_text)>6:
        return {'status':'INCOMPLETE','reasons':['commit_claim_out_of_bounds']}
    claimed_commits=int(commit_text)
    if re.fullmatch(r'[0-9]+',count_text):
        if len(count_text)>4:
            return {'status':'INCOMPLETE','reasons':['file_claim_out_of_bounds']}
        count=int(count_text)
        if count>3000:
            return {'status':'INCOMPLETE','reasons':['file_claim_out_of_bounds']}
    else:
        count=WORDS.get(count_text.lower())
    scope=matches[4][0]
    if count is None:
        return {'status':'INCOMPLETE','reasons':['unparseable_file_count']}
    seen=set()
    for entry in files:
        if not isinstance(entry,dict):
            return {'status':'INCOMPLETE','reasons':['invalid_file_entry']}
        name,status=entry.get('filename'),entry.get('status')
        if (not isinstance(name,str) or not name or name.startswith('/')
            or '\\' in name or any(part in ('','..','.') for part in name.split('/'))
            or not isinstance(status,str) or status not in ('added','modified','removed','renamed')):
            return {'status':'INCOMPLETE','reasons':['invalid_file_entry']}
        if name in seen:
            return {'status':'INCOMPLETE','reasons':['duplicate_file_entry']}
        seen.add(name)
    reasons=[]
    if base!=claimed_base:reasons.append('base_sha_drift')
    if head!=claimed_head:reasons.append('head_sha_drift')
    if commits!=claimed_commits:reasons.append('commit_count_drift')
    if len(files)!=count:reasons.append('file_count_drift')
    extension=EXT[kind.upper()]
    if any(f['status']!='added' or not f['filename'].endswith(extension) for f in files):
        reasons.append('file_kind_drift')
    if any(not f['filename'].startswith(scope) for f in files):
        reasons.append('path_scope_drift')
    return {'status':'DRIFT' if reasons else 'CONSISTENT','reasons':reasons,
            'observed_files':len(files),'claimed_files':count,
            'observed_commits':commits,'claimed_commits':claimed_commits}
