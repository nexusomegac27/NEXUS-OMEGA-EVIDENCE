import hashlib,importlib.util,pathlib,tempfile,unittest
p=pathlib.Path(__file__).resolve().parent.parent/'build_gate_release_v2.py'
spec=importlib.util.spec_from_file_location('release_builder',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestManifestBuilder(unittest.TestCase):
 def test_manifest_complete(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t)
   for name in m.FILES:
    x=root/name;x.parent.mkdir(parents=True,exist_ok=True);x.write_bytes(name.encode())
   out=m.build(root,'a'*40)
   self.assertEqual(len(out['files']),10)
   for name in m.FILES:
    self.assertEqual(out['files'][name]['sha256'],hashlib.sha256(name.encode()).hexdigest())
 def test_reject_moving_ref(self):
  with self.assertRaises(ValueError):m.build('.','main')
 def test_reject_missing_file(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(FileNotFoundError):m.build(t,'a'*40)
 def test_reject_oversized(self):
  with tempfile.TemporaryDirectory() as t:
   root=pathlib.Path(t)
   for name in m.FILES:
    x=root/name;x.parent.mkdir(parents=True,exist_ok=True);x.write_bytes(b'a'*(600001 if name==m.FILES[0] else 1))
   with self.assertRaises(ValueError):m.build(root,'a'*40)
if __name__=='__main__':unittest.main()
