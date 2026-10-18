#!/usr/bin/env python3
"""Fixed independent evaluator for the event-store partition/identity guard.

Written before the candidate patch. Does not import or mutate candidate oracles.
Usage: python independent_evaluator_event_partition_v1.py /path/to/auditor.py
"""
from __future__ import annotations
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

TARGET = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).with_name('archive_continuity_guard_original.py')
spec = importlib.util.spec_from_file_location('auditor_under_test', TARGET)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

BASE_ID = 'NEXUS_RPE_20260901T035600Z_a31f6c20'
BASE_PKG = 'NEXUS_RP_20260901T035600Z_retroactive-symbiotic-backfill_6f1a9c27'
BASE_FILENAME = f'20260901T035600Z_{BASE_ID}.json'

class EventPartitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.as_of = datetime(2026, 10, 18, tzinfo=timezone.utc)
        self.event_dir = self.root/'research/pipeline/events/2026/09/01'
        self.event_dir.mkdir(parents=True)
        structure = self.root/'docs/architecture/REPOSITORY_STRUCTURE.json'
        structure.parent.mkdir(parents=True)
        structure.write_text(json.dumps({'version':'1.7.13','active_research_lanes':{'r16':{'path':'research/r16/alpha','state':'ACTIVE'}}}))
        lane = self.root/'research/r16/alpha'
        lane.mkdir(parents=True)
        (lane/'README.md').write_text('C1\n')
        self.doc = {'event_id':BASE_ID,'package_id':BASE_PKG,'recorded_at_utc':'2026-09-01T03:56:00Z','event_type':'PACKAGE_CREATED','new_state':'INTAKE'}
        self.write(self.event_dir/BASE_FILENAME,self.doc)

    def write(self,path,doc):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')

    def audit(self):
        return g.audit(self.root,self.as_of)

    def assert_event_valid(self,count=1):
        r=self.audit()
        self.assertEqual(r['event_error_count'],0,r['findings'])
        self.assertEqual(r['observed_event_count'],count)

    def assert_event_rejected(self):
        r=self.audit()
        self.assertGreaterEqual(r['event_error_count'],1,r)
        self.assertIn('INVALID_EVENT_RECORDS',{f['code'] for f in r['findings']})

    def test_positive_historical_event(self):
        self.assert_event_valid()

    def test_positive_existing_short_event_id_contract(self):
        old=self.event_dir/BASE_FILENAME;old.unlink()
        self.write(self.event_dir/'20260901T035700Z_E01.json',{'event_id':'E01','package_id':BASE_PKG,'recorded_at_utc':'2026-09-01T03:57:00Z'})
        self.assert_event_valid()

    def test_positive_offset_normalized_to_utc(self):
        self.doc['recorded_at_utc']='2026-09-01T05:56:00+02:00'
        self.write(self.event_dir/BASE_FILENAME,self.doc)
        self.assert_event_valid()

    def test_positive_midnight_utc_day_rollover(self):
        old=self.event_dir/BASE_FILENAME;old.unlink()
        self.doc['recorded_at_utc']='2026-09-02T01:00:00+02:00'
        self.write(self.root/'research/pipeline/events/2026/09/01'/f'20260901T230000Z_{BASE_ID}.json',self.doc)
        self.assert_event_valid()

    def test_negative_filename_event_id_mismatch(self):
        self.doc['event_id']='DIFFERENT_ID'
        self.write(self.event_dir/BASE_FILENAME,self.doc)
        self.assert_event_rejected()

    def test_negative_partition_day_mismatch(self):
        old=self.event_dir/BASE_FILENAME;old.unlink()
        self.write(self.root/'research/pipeline/events/2026/09/02'/BASE_FILENAME,self.doc)
        self.assert_event_rejected()

    def test_negative_filename_clock_mismatch(self):
        old=self.event_dir/BASE_FILENAME;old.unlink()
        self.write(self.event_dir/f'20260901T040000Z_{BASE_ID}.json',self.doc)
        self.assert_event_rejected()

    def test_negative_duplicate_event_id_across_distinct_paths(self):
        self.write(self.event_dir/f'20260901T035601Z_{BASE_ID}.json',dict(self.doc,recorded_at_utc='2026-09-01T03:56:01Z'))
        self.assert_event_rejected()

    def test_existing_negative_invalid_timestamp(self):
        self.doc['recorded_at_utc']='not-a-timestamp'
        self.write(self.event_dir/BASE_FILENAME,self.doc)
        self.assert_event_rejected()

    def test_existing_negative_missing_package_id(self):
        self.doc.pop('package_id')
        self.write(self.event_dir/BASE_FILENAME,self.doc)
        self.assert_event_rejected()

    def test_read_only_bytes_unchanged(self):
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.audit()
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_existing_open_age_not_affected(self):
        self.assertEqual(g.severity('ACTIVE',30,30),'AGING_OPEN_REVIEW')
        self.assertEqual(g.severity('PROCESSED',300,30),'NO_TIME_ESCALATION')


class EventRecordFailClosedTests(EventPartitionTests):
    # Inherits the frozen twelve-case suite, then adds held-out malformed-event cases.
    def test_negative_top_level_json_array(self):
        (self.event_dir/BASE_FILENAME).write_text('[]\n', encoding='utf-8')
        self.assert_event_rejected()

    def test_negative_top_level_json_null(self):
        (self.event_dir/BASE_FILENAME).write_text('null\n', encoding='utf-8')
        self.assert_event_rejected()

    def test_negative_top_level_json_string(self):
        (self.event_dir/BASE_FILENAME).write_text('"malformed event"\n', encoding='utf-8')
        self.assert_event_rejected()

    def test_negative_invalid_utf8(self):
        (self.event_dir/BASE_FILENAME).write_bytes(b'\xff\xfe')
        self.assert_event_rejected()

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(EventRecordFailClosedTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
