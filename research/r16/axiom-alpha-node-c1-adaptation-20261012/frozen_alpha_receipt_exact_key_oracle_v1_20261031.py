#!/usr/bin/env python3
"""Separate black-box subprocess oracle for scoped issue-receipt PR attribution."""
import copy
import json
import subprocess
import sys

ROOT = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'
SHA = ['a' * 40, 'b' * 40, 'c' * 40, 'd' * 40]


def fixture():
    records = []
    for i, n in enumerate(range(228, 232)):
        key = f'PR={ROOT}{n}' if i != 2 else f'OWNER_PR={n}'
        main_key = ('ACTUAL_MAIN_READBACK', 'ACTUAL_MAIN', 'MAIN_AFTER', 'ACTUAL_MAIN_READBACK')[i]
        body = '\n'.join((f'OBJECT=CONTROL_{n}', f'PREDECESSOR_PR={n-1}',
                          'CLAIM_CEILING=C1_DESCRIPTIVE_ONLY', key,
                          f'{main_key}={SHA[i]}', 'SOURCE_REPORT=url', 'SOURCE_REPORT=hash'))
        records.append({'receipt_id': 1000 + i, 'expected_pr': n,
                        'expected_main': SHA[i], 'actor_login': 'nexusomegac27',
                        'body': body})
    return {'schema_version': 'alpha_receipt_exact_key_v1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'records': records}


def run(script, data):
    p = subprocess.run([sys.executable, script], input=json.dumps(data),
                       capture_output=True, text=True, timeout=10)
    return p.returncode, json.loads(p.stdout)


def main(script):
    good = fixture()
    rc, result = run(script, good)
    assert rc == 0 and result['status'] == 'SCOPED_RECEIPT_BINDINGS_MATCH_UNAUTHENTICATED_INPUT'
    assert result['matched_receipts'] == 4 and result['actor_authenticated'] is False
    # Deliberately naive unanchored PR= extraction misattributes the predecessor.
    import re
    assert re.search(r'PR=(\d+)', good['records'][0]['body']).group(1) == '227'
    mutants = [
        ('wrong_target_pr', lambda x: x['records'][0].update(expected_pr=227)),
        ('wrong_main', lambda x: x['records'][0].update(expected_main='f'*40)),
        ('duplicate_receipt', lambda x: x['records'][1].update(receipt_id=1000)),
        ('duplicate_pr', lambda x: x['records'][1].update(expected_pr=228)),
        ('owner_spoof', lambda x: x['records'][1].update(actor_login='external-expert')),
        ('c2_promotion', lambda x: x['records'][0].update(body=x['records'][0]['body'].replace('C1_DESCRIPTIVE_ONLY','C2'))),
        ('missing_pr', lambda x: x['records'][0].update(body=x['records'][0]['body'].split('PR=https')[0])),
        ('duplicate_pr_key', lambda x: x['records'][0].update(body=x['records'][0]['body']+'\nPR='+ROOT+'228')),
        ('predecessor_forgery', lambda x: x['records'][0].update(body=x['records'][0]['body'].replace('PREDECESSOR_PR=227','PREDECESSOR_PR=999'))),
        ('conflicting_main_alias', lambda x: x['records'][0].update(body=x['records'][0]['body']+'\nMAIN_AFTER='+SHA[0])),
        ('wrong_url', lambda x: x['records'][0].update(body=x['records'][0]['body'].replace('github.com/nexusomegac27','github.com/fake-owner'))),
        ('missing_main', lambda x: x['records'][0].update(body=x['records'][0]['body'].replace('ACTUAL_MAIN_READBACK','NO_MAIN'))),
        ('false_predecessor_only', lambda x: x['records'][0].update(body=x['records'][0]['body'].replace('PR='+ROOT+'228','NOT_PR='+ROOT+'228'))),
        ('missing_actor', lambda x: x['records'][0].pop('actor_login')),
    ]
    for name, mutation in mutants:
        x = copy.deepcopy(good)
        mutation(x)
        rc, result = run(script, x)
        assert rc == 2 and result['status'] == 'FAIL_CLOSED', (name, rc, result)
    print(json.dumps({'status':'PASS','positive':4,'negative':len(mutants),
                      'negative_fail_closed':len(mutants),
                      'naive_predecessor_misattribution':'DEMONSTRATED',
                      'source_authentication':'NOT_CLAIMED'}))


if __name__ == '__main__':
    main(sys.argv[1])
