# SPDX-License-Identifier: Apache-2.0
import copy
import hashlib
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from reference import CEILING, GATES, Principal, Store, canonical, cid, decision, parse, validate
from jsonschema import Draft202012Validator, ValidationError

def sample():
    return {'schema_version': 'forum-entry/2', 'author_id': 'human_author',
            'scope': 'Synthetischer Referenztest, kein Forschungsresultat',
            'interpretation': 'Ein Vorschlag bleibt prüfbar.', 'evidence_class': 'PROPOSAL',
            'ambiguity': 'Keine empirische Validierung', 'confidence': 'UNCALIBRATED',
            'evidence_refs': [], 'parent': None, 'claim_ceiling': CEILING}

def reviews(entry):
    peer = {'schema_version': 'forum-review/2', 'kind': 'PEER', 'reviewer_id': 'peer_actor',
            'entry_cid': cid(entry), 'independence': 'DECLARED_NO_CONFLICT',
            'disclosures': 'Synthetische Rolle, keine echte unabhängige Begutachtung',
            'rationale': 'Fixture', 'conclusion': 'SUPPORT', 'peer_review_cid': None,
            'claim_ceiling': CEILING}
    third = dict(peer, kind='THIRD', reviewer_id='third_actor', peer_review_cid=cid(peer))
    return [peer, third]

class CanonicalTests(unittest.TestCase):
    def test_golden_bytes(self):
        expected = '{"a":"ä","z":[true,null,7]}'.encode('utf-8')
        self.assertEqual(canonical({'z': [True, None, 7], 'a': 'ä'}), expected)
        self.assertEqual(cid({'a':'ä','z':[True,None,7]}), 'nexus-forum-cas-v2:sha256:' + hashlib.sha256(expected).hexdigest())

    def test_key_order(self):
        self.assertEqual(cid({'b':1,'a':2}), cid({'a':2,'b':1}))

    def test_mutation_changes_identity(self):
        self.assertNotEqual(cid({'a':1}), cid({'a':2}))

    def test_float_rejected(self):
        for value in [1.0, float('nan'), float('inf')]:
            with self.subTest(value=value), self.assertRaises(ValueError): canonical(value)

    def test_large_integer_rejected(self):
        with self.assertRaises(ValueError): canonical(2 ** 53)

    def test_invalid_unicode_rejected(self):
        with self.assertRaises(UnicodeError): canonical('\ud800')

    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError): parse(b'{"a":1,"a":2}')

    def test_non_ascii_keys_rejected(self):
        with self.assertRaises(ValueError): canonical({'ä':1})

    def test_roundtrip(self):
        obj = sample()
        self.assertEqual(parse(canonical(obj)), obj)

    def test_size_bound(self):
        with self.assertRaises(ValueError): canonical('x' * 1048577)

    def test_depth_bound(self):
        obj = []
        for _ in range(66): obj = [obj]
        with self.assertRaises(ValueError): canonical(obj)

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.entry = sample()
        self.reviews = reviews(self.entry)
        self.actor = Principal('human_author','HUMAN')
        self.gates = dict.fromkeys(GATES, 'PASS')

    def decide(self, action='ACCEPT', **kw):
        args = dict(entry=self.entry, reviews=self.reviews, principal=self.actor,
                    action=action, gates=self.gates, reason='Explizite lokale Entscheidung', acknowledged_dissent=[], process_state='IN_REVIEW')
        args.update(kw)
        return decision(**args)['state']

    def test_positive_local_accept(self):
        self.assertEqual(self.decide(), 'ACCEPTED_LOCAL_C1')

    def test_cannot_accept_unsubmitted_draft(self):
        with self.assertRaisesRegex(ValueError,'SUBMIT_REQUIRED'): self.decide(process_state='DRAFT')

    def test_terminal_state_not_reopened(self):
        for state in ['STOPPED','REJECTED','ACCEPTED_LOCAL_C1']:
            with self.subTest(state=state), self.assertRaisesRegex(ValueError,'TERMINAL_OR_UNKNOWN'):
                self.decide(process_state=state)

    def test_resolved_hold_can_accept(self):
        self.assertEqual(self.decide(process_state='HOLD'), 'ACCEPTED_LOCAL_C1')

    def test_agent_cannot_decide(self):
        with self.assertRaisesRegex(ValueError,'HUMAN_AUTHOR'): self.decide(principal=Principal('human_author','AGENT'))

    def test_other_human_cannot_decide(self):
        with self.assertRaisesRegex(ValueError,'HUMAN_AUTHOR'): self.decide(principal=Principal('other_human','HUMAN'))

    def test_claim_promotion_rejected(self):
        self.entry['claim_ceiling'] = 'C2'
        with self.assertRaises(ValidationError): self.decide()

    def test_token_field_rejected(self):
        self.entry['token_rewards'] = 100
        with self.assertRaises(ValidationError): self.decide()

    def test_missing_scope_rejected(self):
        del self.entry['scope']
        with self.assertRaises(ValidationError): self.decide()

    def test_missing_review_holds(self):
        self.assertEqual(self.decide(reviews=[]), 'HOLD')

    def test_roles_must_differ(self):
        self.reviews[1]['reviewer_id'] = 'peer_actor'
        with self.assertRaisesRegex(ValueError,'ROLE_COLLISION'): self.decide()

    def test_peer_and_third_required(self):
        with self.assertRaisesRegex(ValueError,'REVIEW_ROLES'): self.decide(reviews=[self.reviews[0]]*2)

    def test_revision_invalidates_review(self):
        self.entry['interpretation'] = 'Neue Version'
        with self.assertRaisesRegex(ValueError,'STALE_OR_UNBOUND'): self.decide()

    def test_third_binds_peer_version(self):
        self.reviews[0]['rationale'] = 'Neue Begründung'
        with self.assertRaisesRegex(ValueError,'STALE_OR_UNBOUND'): self.decide()

    def test_undeclared_independence_holds(self):
        self.reviews[1]['independence'] = 'UNDECLARED'
        self.assertEqual(self.decide(), 'HOLD')

    def test_conflict_holds(self):
        self.reviews[1]['independence'] = 'DECLARED_CONFLICT'
        self.assertEqual(self.decide(), 'HOLD')

    def test_unresolved_review_holds(self):
        self.reviews[1]['conclusion'] = 'UNRESOLVED'
        self.assertEqual(self.decide(), 'HOLD')

    def test_dissent_not_silenced(self):
        self.reviews[1]['conclusion'] = 'DISSENT'
        with self.assertRaisesRegex(ValueError,'DISSENT_NOT_ACKNOWLEDGED'): self.decide()
        self.assertEqual(self.decide(acknowledged_dissent=[cid(self.reviews[1])]), 'ACCEPTED_LOCAL_C1')

    def test_unknown_gate_holds(self):
        self.gates['source_binding'] = 'UNKNOWN'
        self.assertEqual(self.decide(), 'HOLD')

    def test_hard_fail_cannot_be_averaged(self):
        self.gates['negative_fixtures'] = 'FAIL'
        self.assertEqual(self.decide(), 'BLOCKED')

    def test_absent_gate_rejected(self):
        with self.assertRaisesRegex(ValueError,'INVALID_GATE'): self.decide(gates={})

    def test_extra_score_rejected(self):
        self.gates['trust_score'] = 100
        with self.assertRaisesRegex(ValueError,'INVALID_GATE'): self.decide()

    def test_stop_does_not_require_review(self):
        self.assertEqual(self.decide(action='STOP',reviews=[],gates={}), 'STOPPED')

    def test_reject_does_not_require_consensus(self):
        self.assertEqual(self.decide(action='REJECT',reviews=[],gates={}), 'REJECTED')

    def test_hold_is_not_truth(self):
        self.assertEqual(self.decide(action='HOLD'), 'HOLD')

    def test_no_automatic_promotion(self):
        with self.assertRaisesRegex(ValueError,'UNKNOWN_ACTION'): self.decide(action='PROMOTE')

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nexus-forum-reference-')
        self.path = str(Path(self.temp.name) / 'store.sqlite')
        self.store = Store(self.path)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_restart_replay(self):
        first = self.store.append('entry.created', sample(), None, 'req1')
        last = self.store.append('dissent.recorded', {'reason':'Ungeklärt'}, first, 'req2')
        before = self.store.replay(last)
        self.store.close()
        self.store = Store(self.path)
        self.assertEqual(self.store.replay(last), before)
        self.assertEqual(len(before), 2)

    def test_idempotent_retry(self):
        key = self.store.append('entry.created',sample(),None,'req1')
        self.assertEqual(self.store.append('entry.created',sample(),None,'req1'), key)
        self.assertEqual(len(self.store.replay(key)), 1)

    def test_idempotency_conflict(self):
        self.store.append('entry.created',sample(),None,'req1')
        with self.assertRaisesRegex(ValueError,'IDEMPOTENCY_CONFLICT'):
            self.store.append('entry.created',{'changed':True},None,'req1')

    def test_stale_head_rolls_back(self):
        key = self.store.append('entry.created',sample(),None,'req1')
        count = self.store.db.execute('SELECT COUNT(*) FROM objects').fetchone()[0]
        with self.assertRaisesRegex(ValueError,'STALE_HEAD'):
            self.store.append('entry.created',{'new':True},None,'req2')
        self.assertEqual(self.store.head(), key)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM objects').fetchone()[0],count)

    def test_two_connections_no_silent_overwrite(self):
        other = Store(self.path)
        try:
            self.store.append('entry.created',sample(),None,'req1')
            with self.assertRaisesRegex(ValueError,'STALE_HEAD'):
                other.append('entry.created',sample(),None,'req2')
        finally: other.close()

    def test_sql_update_and_delete_denied(self):
        self.store.append('entry.created',sample(),None,'req1')
        for table in ['events','objects']:
            with self.subTest(table=table):
                with self.assertRaises(sqlite3.IntegrityError): self.store.db.execute('DELETE FROM '+table)
                col = 'request_key' if table == 'events' else 'cid'
                with self.assertRaises(sqlite3.IntegrityError): self.store.db.execute('UPDATE '+table+' SET '+col+'=?',('changed',))

    def test_expected_checkpoint_required(self):
        self.store.append('entry.created',sample(),None,'req1')
        with self.assertRaisesRegex(ValueError,'CHECKPOINT_MISMATCH'): self.store.replay(None)

    def test_tampered_bytes_detected(self):
        self.store.append('entry.created',sample(),None,'req1')
        # Simulate privileged attacker who bypasses SQL trigger, not a supported operation.
        self.store.db.execute('DROP TRIGGER objects_no_update')
        self.store.db.execute('UPDATE objects SET bytes=? WHERE cid=?',(b'{}',cid(sample())))
        with self.assertRaisesRegex(ValueError,'CAS_CORRUPTION'): self.store.replay(self.store.head())

    def test_missing_object_denied(self):
        with self.assertRaisesRegex(ValueError,'MISSING_OBJECT'): self.store.get(cid(sample()))

class ArtifactTests(unittest.TestCase):
    def test_schemas_well_formed(self):
        for name in ['entry','review']:
            Draft202012Validator.check_schema(json.loads((ROOT/'schema'/f'{name}.schema.json').read_text(encoding='utf-8')))

    def test_input_manifest_evidence(self):
        audit=json.loads((ROOT/'validation/INPUT_AUDIT.json').read_text(encoding='utf-8'))
        self.assertTrue(all(row['match'] for row in audit['grok_manifest']))
        self.assertTrue(all(row['match'] for row in audit['order_manifest']))
        self.assertFalse(audit['review_summary_matches_supplied_grok'])
        for row in audit['supplement_bindings']:
            self.assertEqual(row['actual_sha256'],row['expected_sha256'])
            self.assertNotEqual(row['actual_bytes'],row['expected_bytes'])

    def test_design_token_contrast(self):
        t=json.loads((ROOT/'examples/ui-tokens.json').read_text())
        def luminance(color):
            channels=[int(color[i:i+2],16)/255 for i in [1,3,5]]
            c=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in channels]
            return sum(x*y for x,y in zip(c,[0.2126,0.7152,0.0722]))
        for bg in ['background','surface']:
            for fg in ['text','muted','accent','focus','error']:
                hi,lo=sorted([luminance(t[fg]),luminance(t[bg])],reverse=True)
                with self.subTest(fg=fg,bg=bg): self.assertGreaterEqual((hi+0.05)/(lo+0.05),4.5)

if __name__ == '__main__':
    unittest.main()
