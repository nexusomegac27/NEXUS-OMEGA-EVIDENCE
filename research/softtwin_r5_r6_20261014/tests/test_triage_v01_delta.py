"""One-defect, disposable POSIX sandbox cases. NO NETWORK OR SUBPROCESS."""
from pathlib import Path
import hashlib
import os
import stat
import tempfile
import unittest
import zipfile
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import nexus_artifact_triage_v01 as m

CASE='NEXUS_R5_HARDENING_FIXTURE_01'

class TriageR5Delta(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name);self.p=self.root/'a.zip'
    def mz(self,names):
        with zipfile.ZipFile(self.p,'w') as z:
            for x in names:z.writestr(x,b'x')
    def check_denied(self,pattern):
        with self.assertRaisesRegex(m.Denied,pattern):m.triage(self.root,self.p,CASE)
    def test_d01_cross_platform_casefold_duplicate_denied(self):
        self.mz(['A/x.txt','a/x.txt']);self.check_denied('ZIP_PATH')
    def test_d02_win_reserved_CON_component_denied(self):
        self.mz(['CON/a.txt']);self.check_denied('ZIP_PATH')
    def test_d03_win_reserved_COM9_extension_denied(self):
        self.mz(['COM9.txt']);self.check_denied('ZIP_PATH')
    def test_d04_win_colon_ads_denied(self):
        self.mz(['safe/a:stream']);self.check_denied('ZIP_PATH')
    def test_d05_cross_platform_unicode_normalization_duplicate_denied(self):
        self.mz(['e\u0301/a','é/a']);self.check_denied('ZIP_PATH')
    def test_d06_file_directory_collision_denied(self):
        self.mz(['a','a/b']);self.check_denied('ZIP_FILE_DIRECTORY_PREFIX_COLLISION')
    def test_d07_special_unix_file_type_denied(self):
        info=zipfile.ZipInfo('odd');info.create_system=3;info.external_attr=(0o160000<<16)
        with zipfile.ZipFile(self.p,'w') as z:z.writestr(info,b'x')
        self.check_denied('ZIP_UNSAFE_FILE_TYPE')
    def test_d08_local_vs_central_name_mismatch_denied(self):
        self.mz(['safe.txt']);raw=bytearray(self.p.read_bytes());self.assertEqual(raw.find(b'safe.txt'),30)
        raw[30:38]=b'evil.txt';self.p.write_bytes(raw)
        self.check_denied('ZIP_LOCAL_CENTRAL_MISMATCH')
    def test_d09_hash_summary_binds_same_captured_bytes_despite_path_mutation(self):
        self.mz(['first']);old=self.p.read_bytes()
        alt=self.root/'alt.zip'
        with zipfile.ZipFile(alt,'w') as z:z.writestr('second',b'2');z.writestr('third',b'3')
        original=m._validate_zip_bytes
        def swap_then_validate(snapshot):
            self.p.write_bytes(alt.read_bytes())
            return original(snapshot)
        with patch.object(m,'_validate_zip_bytes',side_effect=swap_then_validate):
            record=m.triage(self.root,self.p,CASE)
        self.assertEqual(record['source_sha256'],hashlib.sha256(old).hexdigest())
        self.assertEqual(record['zip_summary']['entries'],1)
        self.assertTrue(record['zip_summary']['zip_metadata_bound_to_source_bytes'])
    @unittest.skipUnless(hasattr(os,'mkfifo'),'POSIX FIFO only')
    def test_d10_fifo_is_denied_without_blocking(self):
        fifo=self.root/'a.zip';os.mkfifo(fifo)
        self.check_denied('NOT_REGULAR_FILE')
    def test_d11_final_symlink_denied(self):
        source=self.root/'real';source.write_bytes(b'SAFE')
        self.p.symlink_to(source)
        self.check_denied('SYMLINK')
    def test_d12_parent_symlink_denied(self):
        source=self.root/'real';source.mkdir();(source/'x').write_bytes(b'SAFE')
        (self.root/'linked').symlink_to(source,target_is_directory=True)
        with self.assertRaises(m.Denied):m.triage(self.root,self.root/'linked/x',CASE)
    def test_d13_parent_swap_after_anchored_open_keeps_inside_bytes(self):
        approved=self.root/'approved';slot=approved/'slot';slot.mkdir(parents=True)
        target=slot/'a.bin';target.write_bytes(b'INSIDE')
        outside=self.root/'outside';outside.mkdir();(outside/'a.bin').write_bytes(b'OUTSIDE')
        realopen=m.os.open
        swapped=False
        def intercept(path,flags,*args,**kwargs):
            nonlocal swapped
            if path=='a.bin' and 'dir_fd' in kwargs and not swapped:
                slot.rename(approved/'old_slot')
                slot.symlink_to(outside,target_is_directory=True)
                swapped=True
            return realopen(path,flags,*args,**kwargs)
        with patch.object(m.os,'open',side_effect=intercept):
            r=m.triage(approved,target,CASE)
        self.assertTrue(swapped)
        self.assertEqual(r['source_sha256'],hashlib.sha256(b'INSIDE').hexdigest())
    def test_d14_zip_512_boundary_kept(self):
        self.mz([f'f{i}' for i in range(512)])
        self.assertEqual(m.triage(self.root,self.p,CASE)['zip_summary']['entries'],512)
    def test_d15_zip_513_boundary_denied(self):
        self.mz([f'f{i}' for i in range(513)]);self.check_denied('ZIP_ENTRY_COUNT_LIMIT')
    def test_d16_unknown_bytes_no_behavior_claim(self):
        self.p.write_bytes(b'opaque input')
        r=m.triage(self.root,self.p,CASE)
        self.assertFalse(r['execution_performed']);self.assertFalse(r['network_called']);self.assertIn('NOT_A_SANDBOX',r['unresolved'])
    def test_d17_no_unsafe_extract_and_no_model(self):
        self.mz(['safe.txt']);r=m.triage(self.root,self.p,CASE)
        self.assertFalse(r['zip_summary']['entries_extracted']);self.assertEqual(r['authority'],'NONE_NOT_AN_AUTHORIZATION_GATE')
    def test_d18_root_symlink_denied(self):
        self.p.write_bytes(b'123');alias=self.root.parent/'alias_triage_r5'
        # Avoid creating a shared stable alias: use a private subfolder path inside temp.
        holder=self.root/'holder';holder.mkdir();lnk=self.root/'alias';lnk.symlink_to(holder,target_is_directory=True)
        (holder/'file').write_bytes(b'ABC')
        with self.assertRaisesRegex(m.Denied,'ROOT_UNAVAILABLE_OR_SYMLINK'):
            m.triage(lnk,lnk/'file',CASE)
    def test_d19_local_method_tamper_denied(self):
        self.mz(['a'])
        raw=bytearray(self.p.read_bytes());raw[8:10]=b'\x08\x00';self.p.write_bytes(raw)
        self.check_denied('ZIP_LOCAL_CENTRAL_MISMATCH')
    def test_d20_explicit_no_windows_portability_claim(self):
        self.p.write_bytes(b'123')
        self.assertIn('NO_WINDOWS_NATIVE_HANDLE_VALIDATION',m.triage(self.root,self.p,CASE)['unresolved'])

if __name__=='__main__':unittest.main()
