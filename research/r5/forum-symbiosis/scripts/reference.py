# SPDX-License-Identifier: Apache-2.0
"""Isolated executable blueprint. NOT an HTTP server or authenticated production API."""
import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'nexus-forum-cas-v2:sha256:'
CEILING = 'C1_DESCRIPTIVE_ONLY'
GATES = {'source_binding', 'negative_fixtures', 'scope_review', 'policy_review'}

def canonical(value):
    """NEXUS restricted profile, not RFC8785/JCS and not legacy R10 v1."""
    def check(v, depth=0):
        if depth > 64:
            raise ValueError('DEPTH')
        if v is None or type(v) is bool:
            return
        if type(v) is int and abs(v) <= 9007199254740991:
            return
        if type(v) is str:
            v.encode('utf-8', errors='strict')
            return
        if type(v) is list:
            for child in v:
                check(child, depth + 1)
            return
        if type(v) is dict:
            for key, child in v.items():
                if type(key) is not str or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
                    raise ValueError('ASCII_KEYS_REQUIRED')
                check(child, depth + 1)
            return
        raise ValueError('UNSUPPORTED_JSON_VALUE')
    check(value)
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    if len(data) > 1048576:
        raise ValueError('OBJECT_TOO_LARGE')
    return data

def parse(data):
    if len(data) > 1048576:
        raise ValueError('OBJECT_TOO_LARGE')
    def pairs(items):
        d = {}
        for key, value in items:
            if key in d:
                raise ValueError('DUPLICATE_KEY')
            d[key] = value
        return d
    obj = json.loads(data.decode('utf-8'), object_pairs_hook=pairs)
    canonical(obj)
    return obj

def cid(value):
    return PREFIX + hashlib.sha256(canonical(value)).hexdigest()

def validate(value, name):
    # Dependency is used only for schema tests and decision contract validation.
    from jsonschema import Draft202012Validator
    schema = json.loads((ROOT / 'schema' / (name + '.schema.json')).read_text(encoding='utf-8'))
    canonical(value)
    Draft202012Validator(schema).validate(value)

@dataclass(frozen=True)
class Principal:
    """Constructed by a trusted adapter, NEVER from client-supplied role fields."""
    actor_id: str
    kind: str

def decision(entry, reviews, principal, action, gates, reason, acknowledged_dissent, process_state):
    """Pure rule evaluator. Authentication and gate evidence are caller obligations."""
    validate(entry, 'entry')
    if principal.actor_id != entry['author_id'] or principal.kind != 'HUMAN':
        raise ValueError('HUMAN_AUTHOR_REQUIRED')
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError('REASON_REQUIRED')
    if process_state not in {'DRAFT', 'IN_REVIEW', 'HOLD', 'BLOCKED'}:
        raise ValueError('TERMINAL_OR_UNKNOWN_STATE')
    if action in {'STOP', 'REJECT'}:
        return {'state': 'STOPPED' if action == 'STOP' else 'REJECTED', 'claim_ceiling': CEILING}
    if action not in {'ACCEPT', 'HOLD'}:
        raise ValueError('UNKNOWN_ACTION')
    if action == 'HOLD':
        return {'state': 'HOLD', 'claim_ceiling': CEILING}
    if process_state == 'DRAFT':
        raise ValueError('SUBMIT_REQUIRED')
    if set(gates) != GATES or any(v not in {'PASS', 'FAIL', 'UNKNOWN'} for v in gates.values()):
        raise ValueError('INVALID_GATE_SET')
    if 'FAIL' in gates.values():
        return {'state': 'BLOCKED', 'claim_ceiling': CEILING}
    if 'UNKNOWN' in gates.values():
        return {'state': 'HOLD', 'claim_ceiling': CEILING}
    if len(reviews) != 2:
        return {'state': 'HOLD', 'claim_ceiling': CEILING}
    for review in reviews:
        validate(review, 'review')
    kinds = {r['kind']: r for r in reviews}
    if set(kinds) != {'PEER', 'THIRD'}:
        raise ValueError('REVIEW_ROLES_REQUIRED')
    peer, third = kinds['PEER'], kinds['THIRD']
    ids = {entry['author_id'], peer['reviewer_id'], third['reviewer_id']}
    if len(ids) != 3:
        raise ValueError('ROLE_COLLISION')
    if any(r['entry_cid'] != cid(entry) for r in reviews) or third['peer_review_cid'] != cid(peer):
        raise ValueError('STALE_OR_UNBOUND_REVIEW')
    if any(r['independence'] != 'DECLARED_NO_CONFLICT' or r['conclusion'] == 'UNRESOLVED' for r in reviews):
        return {'state': 'HOLD', 'claim_ceiling': CEILING}
    dissent = {cid(r) for r in reviews if r['conclusion'] == 'DISSENT'}
    if not dissent.issubset(set(acknowledged_dissent)):
        raise ValueError('DISSENT_NOT_ACKNOWLEDGED')
    return {'state': 'ACCEPTED_LOCAL_C1', 'claim_ceiling': CEILING}

class Store:
    """Single local database. Triggers protect normal use, not a malicious file owner."""
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=2, isolation_level=None)
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript((ROOT / 'schema/store.sql').read_text(encoding='utf-8'))

    def close(self):
        self.db.close()

    def head(self):
        row = self.db.execute('SELECT cid FROM events ORDER BY seq DESC LIMIT 1').fetchone()
        return row[0] if row else None

    def _put(self, obj):
        key, data = cid(obj), canonical(obj)
        old = self.db.execute('SELECT bytes FROM objects WHERE cid=?', (key,)).fetchone()
        if old and old[0] != data:
            raise ValueError('CAS_COLLISION_OR_CORRUPTION')
        if not old:
            self.db.execute('INSERT INTO objects VALUES (?,?)', (key, data))
        return key

    def get(self, key):
        row = self.db.execute('SELECT bytes FROM objects WHERE cid=?', (key,)).fetchone()
        if not row:
            raise ValueError('MISSING_OBJECT')
        obj = parse(row[0])
        if canonical(obj) != row[0] or cid(obj) != key:
            raise ValueError('CAS_CORRUPTION')
        return obj

    def append(self, kind, payload, expected_head, request_key):
        # Internal storage primitive. Policy must run BEFORE calling it.
        if not re.fullmatch(r'[a-z][a-z0-9_.-]{1,63}', kind):
            raise ValueError('EVENT_KIND')
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,128}', request_key):
            raise ValueError('REQUEST_KEY')
        request = {'kind': kind, 'payload': payload, 'expected_head': expected_head}
        digest = cid(request)
        self.db.execute('BEGIN IMMEDIATE')
        try:
            prior = self.db.execute('SELECT cid,request_digest FROM events WHERE request_key=?', (request_key,)).fetchone()
            if prior:
                if prior[1] != digest:
                    raise ValueError('IDEMPOTENCY_CONFLICT')
                self.get(prior[0])
                self.db.execute('COMMIT')
                return prior[0]
            if self.head() != expected_head:
                raise ValueError('STALE_HEAD')
            payload_cid = self._put(payload)
            seq = self.db.execute('SELECT COALESCE(MAX(seq),0)+1 FROM events').fetchone()[0]
            event = {'seq': seq, 'previous_cid': expected_head, 'kind': kind,
                     'payload_cid': payload_cid, 'request_key': request_key,
                     'request_digest': digest, 'claim_ceiling': CEILING}
            key = self._put(event)
            self.db.execute('INSERT INTO events VALUES (?,?,?,?,?)', (seq, key, expected_head, request_key, digest))
            self.db.execute('COMMIT')
            return key
        except BaseException:
            self.db.execute('ROLLBACK')
            raise

    def replay(self, expected_head):
        previous, output = None, []
        for seq, key, parent, request_key, digest in self.db.execute('SELECT * FROM events ORDER BY seq').fetchall():
            event = self.get(key)
            if (seq != len(output) + 1 or parent != previous or event['seq'] != seq
                    or event['previous_cid'] != parent or event['request_key'] != request_key
                    or event['request_digest'] != digest or event['claim_ceiling'] != CEILING):
                raise ValueError('CHAIN_CORRUPTION')
            payload = self.get(event['payload_cid'])
            if cid({'kind': event['kind'], 'payload': payload, 'expected_head': parent}) != digest:
                raise ValueError('REQUEST_CORRUPTION')
            output.append({'event': event, 'payload': payload})
            previous = key
        if previous != expected_head:
            raise ValueError('CHECKPOINT_MISMATCH')
        return output
