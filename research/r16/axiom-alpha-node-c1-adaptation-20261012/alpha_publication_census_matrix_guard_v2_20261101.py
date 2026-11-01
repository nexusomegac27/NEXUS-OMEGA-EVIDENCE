"""Isolated C1 structural matrix guard. Does not fetch or authenticate GitHub originals.
Versioned successor to frozen_alpha_publication_census_oracle_v1_20261101.py.
"""
import json
import sys

CHAIN = [
 ('245','f17196d26faa03650709601f8fecea6c50cc657d','ca8b2f9d7a5cf7371611690c2c4a52e5904f1e67',6547058731,3),
 ('247','ca8b2f9d7a5cf7371611690c2c4a52e5904f1e67','6363cd0ac7979bc4adea6407ca950baf1cbb3cd3',6547281868,3),
 ('248','6363cd0ac7979bc4adea6407ca950baf1cbb3cd3','8036ffdb2985c688705f2d29f594b8dd757a5f55',6548115987,3),
 ('249','8036ffdb2985c688705f2d29f594b8dd757a5f55','cfad6f9ad1f51efc2114249f14228aaa3a1c4cbd',6548805508,3),
 ('250','cfad6f9ad1f51efc2114249f14228aaa3a1c4cbd','8bb1861d8d548a3bec172ae892b4cda0e20ee559',6549272854,3),
 ('251','8bb1861d8d548a3bec172ae892b4cda0e20ee559','ec887632a4f1659a29c01f4db8bbf1cc79c30ae6',6549786500,3),
 ('252','ec887632a4f1659a29c01f4db8bbf1cc79c30ae6','daffb9c7f80eb3f5d12af48e66dd5306d11cec1e',6550946364,2),
]
REQUIRED_FILE_FLAGS = ('sha_match','blob_match','bytes_match')

def check(records):
    if not isinstance(records, list) or len(records) != len(CHAIN):
        return False
    for i, (record, expected) in enumerate(zip(records, CHAIN)):
        if not isinstance(record, dict):
            return False
        pr, parent, main, receipt, file_count = expected
        if record.get('pr') != pr or record.get('parent') != parent or record.get('main') != main:
            return False
        if i and parent != CHAIN[i-1][2]:
            return False
        if type(record.get('receipt_id')) is not int or record['receipt_id'] != receipt:
            return False
        if record.get('additive') is not True or record.get('signature') is not True:
            return False
        files = record.get('files')
        if not isinstance(files, list) or len(files) != file_count:
            return False
        if any(not isinstance(f, dict) or any(f.get(k) is not True for k in REQUIRED_FILE_FLAGS)
               for f in files):
            return False
        checks = record.get('checks')
        if not isinstance(checks, list) or len(checks) != 8 or any(c != 'success' for c in checks):
            return False
    return True

def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result

if __name__ == '__main__':
    try:
        records = json.loads(sys.stdin.read(), object_pairs_hook=reject_duplicates)
        accepted = check(records)
    except (ValueError, TypeError, RecursionError, UnicodeError):
        accepted = False
    print(json.dumps({'accepted': accepted, 'scope': 'STRUCTURAL_MATRIX_ONLY_NO_GITHUB_READBACK'}))
