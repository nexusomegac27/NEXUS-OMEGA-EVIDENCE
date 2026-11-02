"""Frozen, standalone negative oracle for an isolated GitHub comment REST preflight.

Expected outcomes are independent of the candidate implementation. Commit
this oracle first; never edit it to accommodate the candidate.
"""
import copy
import hashlib
import importlib.util
import json
import sys

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ID = 6585520284
BODY = 'synthetic public-safe receipt'
PIN = hashlib.sha256(BODY.encode()).hexdigest()

def fixture():
    return {'id': ID,
            'url': f'https://api.github.com/repos/{REPO}/issues/comments/{ID}',
            'html_url': f'https://github.com/{REPO}/issues/93#issuecomment-{ID}',
            'issue_url': f'https://api.github.com/repos/{REPO}/issues/93',
            'user': {'login': 'nexusomegac27', 'id': 281316431},
            'created_at': '2026-11-02T18:52:48Z', 'body': BODY}

def run(path):
    spec = importlib.util.spec_from_file_location('isolated_candidate', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = []
    def check(name, record, expected_status, expected_reason, id=ID, pin=PIN, actor='nexusomegac27'):
        try:
            got = module.verify(record, id, pin, actor)
            ok = (got.get('status') == expected_status and got.get('reason') == expected_reason
                  and got.get('project_rate') == 'NOT_COMPUTABLE'
                  and got.get('evidence_class') == 'SUPPLIED_REST_RECORD_NOT_INDEPENDENTLY_AUTHENTICATED')
            cases.append({'name': name, 'pass': ok, 'status': got.get('status'), 'reason': got.get('reason')})
        except Exception as exc:
            cases.append({'name': name, 'pass': False, 'error': type(exc).__name__})
    good = 'API_RECORD_SHAPE_AND_BODY_PIN_MATCH_DECLARED_ONLY'
    caveat = 'NO_INDEPENDENT_API_TRANSPORT_AUTHENTICATION'
    bad = 'NOT_COMPUTABLE'
    a = fixture()
    check('valid_synthetic_positive', a, good, caveat)
    for name, key, value, reason in [
        ('id_alias', 'id', ID+1, 'COMMENT_ID_MISMATCH'),
        ('wrong_api_repository', 'url', f'https://api.github.com/repos/other/repo/issues/comments/{ID}', 'COMMENT_API_URL_MISMATCH'),
        ('wrong_html_issue', 'html_url', f'https://github.com/{REPO}/issues/94#issuecomment-{ID}', 'COMMENT_HTML_URL_MISMATCH'),
        ('wrong_html_host', 'html_url', f'https://evil.invalid/{REPO}/issues/93#issuecomment-{ID}', 'COMMENT_HTML_URL_MISMATCH'),
        ('wrong_issue_url', 'issue_url', f'https://api.github.com/repos/{REPO}/issues/94', 'COMMENT_ISSUE_URL_MISMATCH'),
        ('tampered_body', 'body', BODY+' altered', 'BODY_SHA256_MISMATCH'),
        ('missing_body', 'body', None, 'BODY_NOT_PRESENT'),
        ('bad_timestamp', 'created_at', 'tomorrow', 'CREATION_TIME_INVALID'),
        ('bool_id', 'id', True, 'COMMENT_ID_MISMATCH'),
    ]:
        x = copy.deepcopy(a); x[key] = value; check(name, x, bad, reason)
    x=copy.deepcopy(a); x['user']['login']='fake-expert'; check('actor_substitution',x,bad,'ACTOR_MISMATCH')
    x=copy.deepcopy(a); x['user']['id']=True; check('bool_actor_id',x,bad,'ACTOR_ID_INVALID')
    x=copy.deepcopy(a); x.pop('user'); check('missing_actor',x,bad,'ACTOR_NOT_PRESENT')
    check('missing_independent_pin',a,bad,'INDEPENDENT_BODY_PIN_MISSING_OR_INVALID',pin='UNKNOWN')
    check('missing_api_record',None,bad,'RECORD_NOT_OBJECT')
    check('falsifier_self_consistent_forgery', {**a,'body':'forged'},good,caveat,pin=hashlib.sha256(b'forged').hexdigest())
    return cases

if __name__ == '__main__':
    rows=run(sys.argv[1]); passed=sum(x['pass'] for x in rows)
    print(json.dumps({'passed':passed,'total':len(rows),'rows':rows},sort_keys=True))
    sys.exit(0 if passed==len(rows) else 1)
