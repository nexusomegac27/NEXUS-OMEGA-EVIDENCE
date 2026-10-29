#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen C1 inventory oracle: caller data only, no GitHub authentication."""
import copy
import unittest

SOURCES = [
 ('alpha_pr191_195_incremental_original_byte_census_c1_report_20261029.md',8858,'b0b855923a3a692da70652b05735fa88251fcfdd1cb8d7e5fadb4372d15d2fc1','59d576395d428d63d192ebaa543c1c88df041ed1'),
 ('alpha_issue93_v7_dependency_fixity_preflight_c1_report_20261029.md',5603,'38fbeabb2b4421d754877b72f9c50ab3a306889bdfd2211427179a481d22cae3','33a819d59018db4770ce7985dc7a38ace72a43af'),
 ('alpha_issue93_v7_dependency_fixity_preflight_v1_20261029.py',4194,'0fb4f5408d4c61d3a2e4c9bd160cc63afe68b077febbdd288e757b0fb324af23','80ed3eee7bf66c8076ce4f06c1eac5e9904ded48'),
 ('frozen_issue93_v7_dependency_fixity_oracle_v1_20261029.py',4938,'249e51a98d810bf5ddc37f0b9de22195706c9591ae20ad6eb64c678f3c47023b','9534bc535643b73c732644177236db24b3f6a313'),
]
PR = [
 (184,'05748765ab35d87d6bfa79377a97d7c0ff2c2807',6485768210),
 (186,'3c68b978d2d3273c4684b2dafa33dfac5376cc7e',6486339190),
 (187,'09f517e544056c7217a800f1f596cedb356db2c2',6486832437),
 (188,'8b7ac2a34175f520f7fd9c1fe738cb902f0e6c41',6487895710),
 (189,'1208a338714c78951371fa431e13261726c6b590',6489031228),
 (190,'5a02976c63067f451bbac111f8d7ff287671dc54',6489508368),
 (191,'d26379d34e95659572495456eedc525f2f5540af',6492574334),
 (192,'f7379d164d6f55120f4f80372ba3cb115a12f77f',6495585764),
 (193,'c7a69c537616ad9da142a83b25da2c43c3efaf4f',6496658656),
 (194,'e0af98acaed7ea3357fcb5169a4ec3a31ba8ff5d',6498003720),
 (195,'1a824816506b917bac5027291f47edb9ff228fc1',6499548718),
 (196,'959cfe7e13db98735e4b3d7ec26d2d0ce7d5cbe7',6500402037),
 (197,'076d763dc8bb9aae26a8507aae0e7567eac9ee3e',6503078382),
]

def fixture():
    return {'files':[list(x)+[x[3]] for x in SOURCES],
            'prs':[list(x)+[x[1],'nexusomegac27',True] for x in PR],
            'pr185_merged':False,'ahead':12,'behind':0,
            'previous_files':31,'previous_bytes':137572,
            'total_files':35,'total_bytes':161165}

def audit(d):
    if type(d) is not dict or set(d)!=set(fixture()): raise ValueError('SCHEMA')
    if len(d['files'])!=4 or len(d['prs'])!=13: raise ValueError('COUNT')
    if d['files']!=fixture()['files']: raise ValueError('FILE_FIXITY')
    if d['prs']!=fixture()['prs']: raise ValueError('PR_RECEIPT')
    if d['pr185_merged'] is not False: raise ValueError('OPEN_NEGATIVE_CONTROL')
    if (d['ahead'],d['behind'])!=(12,0): raise ValueError('ANCESTRY')
    if (d['previous_files'],d['previous_bytes'])!=(31,137572): raise ValueError('PREVIOUS')
    if d['total_files']!=d['previous_files']+len(d['files']): raise ValueError('TOTAL_FILES')
    if d['total_bytes']!=d['previous_bytes']+sum(f[1] for f in d['files']): raise ValueError('TOTAL_BYTES')
    return (4,23593,13,35,161165)

class IndependentFixtureTests(unittest.TestCase):
    def test_positive(self): self.assertEqual(audit(fixture()),(4,23593,13,35,161165))
    def reject(self,mutate):
        d=fixture(); mutate(d)
        with self.assertRaises(ValueError): audit(d)
    def test_wrong_sha(self): self.reject(lambda d:d['files'][0].__setitem__(2,'0'*64))
    def test_wrong_git_blob(self): self.reject(lambda d:d['files'][0].__setitem__(3,'0'*40))
    def test_wrong_api_blob(self): self.reject(lambda d:d['files'][0].__setitem__(4,'0'*40))
    def test_missing_file(self): self.reject(lambda d:d['files'].pop())
    def test_duplicate_file(self): self.reject(lambda d:d['files'].__setitem__(3,copy.deepcopy(d['files'][2])))
    def test_missing_receipt(self): self.reject(lambda d:d['prs'][12].__setitem__(2,0))
    def test_wrong_main(self): self.reject(lambda d:d['prs'][12].__setitem__(3,PR[-2][1]))
    def test_untrusted_actor(self): self.reject(lambda d:d['prs'][12].__setitem__(4,'unknown'))
    def test_false_merge(self): self.reject(lambda d:d.__setitem__('pr185_merged',True))
    def test_wrong_ancestry(self): self.reject(lambda d:d.__setitem__('ahead',11))
    def test_wrong_total(self): self.reject(lambda d:d.__setitem__('total_bytes',161164))

if __name__=='__main__': unittest.main()
