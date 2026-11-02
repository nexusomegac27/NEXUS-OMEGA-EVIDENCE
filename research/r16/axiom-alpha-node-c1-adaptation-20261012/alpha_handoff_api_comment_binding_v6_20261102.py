"""Isolated C1 preflight: bind a supplied GitHub REST issue-comment record.

This does NOT fetch GitHub, authenticate the caller, prove independent
scientific evaluation, or count unattended handoffs. The caller must obtain
and pin the expected body digest from a separate trusted read.
"""
import hashlib
import re

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ISSUE = 93
HEX64 = re.compile(r'^[0-9a-f]{64}$')
UTC = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$')


def verify(record, expected_id, expected_body_sha256, expected_actor=None):
    base = {'status': 'NOT_COMPUTABLE', 'comment_id': None,
            'actor': None, 'body_sha256': None,
            'evidence_class': 'SUPPLIED_REST_RECORD_NOT_INDEPENDENTLY_AUTHENTICATED',
            'project_rate': 'NOT_COMPUTABLE'}
    def fail(reason):
        return {**base, 'reason': reason}
    if not isinstance(record, dict):
        return fail('RECORD_NOT_OBJECT')
    if type(expected_id) is not int or expected_id <= 0:
        return fail('EXPECTED_ID_INVALID')
    if not isinstance(expected_body_sha256, str) or not HEX64.fullmatch(expected_body_sha256):
        return fail('INDEPENDENT_BODY_PIN_MISSING_OR_INVALID')
    if expected_actor is not None and (not isinstance(expected_actor, str) or not expected_actor):
        return fail('EXPECTED_ACTOR_INVALID')
    if type(record.get('id')) is not int or record['id'] != expected_id:
        return fail('COMMENT_ID_MISMATCH')
    expected_url = f'https://api.github.com/repos/{REPO}/issues/comments/{expected_id}'
    expected_html = f'https://github.com/{REPO}/issues/{ISSUE}#issuecomment-{expected_id}'
    expected_issue = f'https://api.github.com/repos/{REPO}/issues/{ISSUE}'
    if record.get('url') != expected_url:
        return fail('COMMENT_API_URL_MISMATCH')
    if record.get('html_url') != expected_html:
        return fail('COMMENT_HTML_URL_MISMATCH')
    if record.get('issue_url') != expected_issue:
        return fail('COMMENT_ISSUE_URL_MISMATCH')
    user = record.get('user')
    if not isinstance(user, dict) or not isinstance(user.get('login'), str) or not user['login']:
        return fail('ACTOR_NOT_PRESENT')
    if type(user.get('id')) is not int or user['id'] <= 0:
        return fail('ACTOR_ID_INVALID')
    if expected_actor is not None and user['login'] != expected_actor:
        return fail('ACTOR_MISMATCH')
    if not isinstance(record.get('created_at'), str) or not UTC.fullmatch(record['created_at']):
        return fail('CREATION_TIME_INVALID')
    if not isinstance(record.get('body'), str):
        return fail('BODY_NOT_PRESENT')
    digest = hashlib.sha256(record['body'].encode('utf-8')).hexdigest()
    if digest != expected_body_sha256:
        return fail('BODY_SHA256_MISMATCH')
    return {**base, 'status': 'API_RECORD_SHAPE_AND_BODY_PIN_MATCH_DECLARED_ONLY',
            'reason': 'NO_INDEPENDENT_API_TRANSPORT_AUTHENTICATION',
            'comment_id': expected_id, 'actor': user['login'], 'body_sha256': digest}
