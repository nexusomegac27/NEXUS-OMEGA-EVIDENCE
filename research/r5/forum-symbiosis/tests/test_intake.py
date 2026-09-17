# SPDX-License-Identifier: Apache-2.0
import io
import sys
import unittest
import zipfile
from unittest.mock import Mock
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_inputs import inspect_archive

class IntakeTests(unittest.TestCase):
    def inspect(self, names):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:
            for name in names: z.writestr(name,b'fixture')
        with zipfile.ZipFile(data) as z: return inspect_archive(z)

    def test_safe_relative_path(self):
        self.assertEqual(self.inspect(['docs/entry.md'])['issues'],[])

    def test_parent_traversal(self):
        self.assertTrue(self.inspect(['../escape'])['issues'])

    def test_absolute_path(self):
        self.assertTrue(self.inspect(['/escape'])['issues'])

    def test_drive_path(self):
        self.assertTrue(self.inspect(['C:/escape'])['issues'])

    def test_backslash(self):
        # ZipFile.writestr normalizes Windows separators; feed raw decoded metadata.
        entry = zipfile.ZipInfo('safe')
        entry.filename = 'docs\\file'
        archive = Mock()
        archive.infolist.return_value = [entry]
        self.assertTrue(inspect_archive(archive)['issues'])

    def test_casefold_duplicate(self):
        self.assertTrue(self.inspect(['docs/A.md','docs/a.md'])['issues'])

    def test_windows_reserved(self):
        self.assertTrue(self.inspect(['docs/CON.txt'])['issues'])

    def test_trailing_dot(self):
        self.assertTrue(self.inspect(['docs/file.'])['issues'])
