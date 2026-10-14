"""R6 new one-defect fixtures for V0.2. NO NETWORK OR SUBPROCESS. Disposable POSIX sandbox only.
Runtime status in the R6 return: NOT_EXECUTED (no Python interpreter in that research environment);
this file is the executable deliverable for the next authorized runtime session."""
from pathlib import Path
import os
import struct
import tempfile
import unittest
import zipfile
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import nexus_artifact_triage_v02 as m

CASE = 'NEXUS_R6_NEW_FIXTURE_01'

class TriageV02New(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory(); self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name); self.p = self.root / 'a.zip'
    def mz(self, names):
        with zipfile.ZipFile(self.p, 'w') as z:
            for x in names: z.writestr(x, b'x')
    def check_denied(self, pattern):
        with self.assertRaisesRegex(m.Denied, pattern): m.triage(self.root, self.p, CASE)

    def test_t01_oversize_denied(self):
        big = self.root / 'big.bin'
        with open(big, 'wb') as fh: fh.truncate(32 * 1024 * 1024 + 1)
        self.assertRaisesRegex(m.Denied, 'FILE_SIZE_LIMIT', m.triage, self.root, big, CASE)

    def test_t02_directory_artifact_denied_as_nonregular(self):
        d = self.root / 'adir'; d.mkdir()
        self.assertRaisesRegex(m.Denied, 'NOT_REGULAR_FILE', m.triage, self.root, d, CASE)

    def test_t03_hardlink_witness_recorded(self):
        f = self.root / 'real.bin'; f.write_bytes(b'SAFE')
        link = self.root / 'link.bin'; os.link(f, link)
        r = m.triage(self.root, link, CASE)
        joined = ' '.join(r['unresolved'])
        self.assertIn('HARDLINK_WITNESS_NLINK_2', joined)

    def test_t04_root_intermediate_symlink_denied(self):
        holder = self.root / 'holder'; (holder / 'data').mkdir(parents=True)
        (holder / 'data' / 'f.bin').write_bytes(b'OUTSIDE_NOMINAL_ROOT')
        alias = self.root / 'alias'; alias.symlink_to(holder, target_is_directory=True)
        root_arg = alias / 'data'
        self.assertRaisesRegex(m.Denied, 'ROOT_UNAVAILABLE_OR_SYMLINK', m.triage, root_arg, root_arg / 'f.bin', CASE)

    def test_t05_writer_restoring_mtime_detected_via_ctime(self):
        f = self.root / 'a.bin'; f.write_bytes(b'\x7fELF\x02' + b'\x00' * 20)
        real_fstat = os.fstat
        calls = {'n': 0}
        def fake_fstat(fd):
            st = real_fstat(fd)
            calls['n'] += 1
            if calls['n'] == 2:
                vals = list(st)
                # emulate a concurrent write: ctime advances, mtime restored by attacker
                idx = {a[0]: i for i, a in enumerate(os.stat_result.__reduce__()[1])} if False else None
                return os.stat_result(tuple(v + 1000000 if i == st.__len__() - 1 else v for i, v in enumerate(st)), st.st_atime_ns, st.st_mtime_ns, st.st_ctime_ns + 1000000)
            return st
        import unittest.mock as mock
        with mock.patch.object(m.os, 'fstat', side_effect=fake_fstat):
            self.assertRaisesRegex(m.Denied, 'FILE_CHANGED_DURING_READ', m.triage, self.root, f, CASE)

    def test_t06_concurrent_growth_detected(self):
        f = self.root / 'a.bin'; f.write_bytes(b'\x7fELF\x02' + b'\x00' * 20)
        real_fstat = os.fstat
        calls = {'n': 0}
        def fake_fstat(fd):
            st = real_fstat(fd)
            calls['n'] += 1
            if calls['n'] == 2:
                return os.stat_result(tuple(v if i != 6 else v + 4 for i, v in enumerate(st)), st.st_atime_ns, st.st_mtime_ns + 1, st.st_ctime_ns + 1)
            return st
        import unittest.mock as mock
        with mock.patch.object(m.os, 'fstat', side_effect=fake_fstat):
            self.assertRaisesRegex(m.Denied, 'FILE_CHANGED_DURING_READ', m.triage, self.root, f, CASE)

    def test_t07_header_offset_out_of_range_denied(self):
        self.mz(['safe.txt'])
        raw = bytearray(self.p.read_bytes())
        c = raw.find(b'PK\x01\x02')
        struct.pack_into('<I', raw, c + 42, len(raw) + 1000)
        self.p.write_bytes(raw)
        self.check_denied('ZIP_LOCAL_HEADER_INVALID')

    def test_t08_inflated_local_data_region_denied(self):
        self.mz(['a.txt'])
        raw = bytearray(self.p.read_bytes())
        c = raw.find(b'PK\x01\x02')
        struct.pack_into('<I', raw, c + 20, len(raw) * 2)
        self.p.write_bytes(raw)
        self.check_denied('ZIP_LOCAL_DATA_REGION_OUT_OF_BOUNDS')

    def test_t09_nested_zip_opaque_no_recursion(self):
        import io
        inner = io.BytesIO()
        with zipfile.ZipFile(inner, 'w') as z: z.writestr('deep.txt', b'deep')
        with zipfile.ZipFile(self.p, 'w') as z: z.writestr('inner.zip', inner.getvalue())
        r = m.triage(self.root, self.p, CASE)
        self.assertEqual(r['zip_summary']['entries'], 1)
        self.assertFalse(r['zip_summary']['entries_extracted'])

    def test_t10_truncated_tail_denied(self):
        self.mz(['a', 'b'])
        raw = self.p.read_bytes()[:-10]
        self.p.write_bytes(raw)
        self.check_denied('ZIP_MALFORMED')

    def test_t11_v02_schema_and_bounds_flag(self):
        self.mz(['ok.txt'])
        r = m.triage(self.root, self.p, CASE)
        self.assertEqual(r['schema'], 'NEXUS_REA_STATIC_TRIAGE_V0_2_C1')
        self.assertTrue(r['zip_summary']['local_data_regions_bounded'])

if __name__ == '__main__': unittest.main()
