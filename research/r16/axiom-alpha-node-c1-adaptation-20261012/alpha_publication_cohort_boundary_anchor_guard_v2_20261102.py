"""C1 isolated candidate: pin the *first* PR boundary in the 274–283 cohort.

Extends the unchanged frozen V1 structural evaluator; no GitHub I/O,
identity attestation, production integration or claim promotion.
"""
import json
import sys
import frozen_alpha_publication_cohort_evaluator_v1_20261102 as prior

FIRST_PARENT = '964fe47c4bdbad599e0689b132ff73c0822f3518'
FIRST_MERGE = '3cc35487e8cae54aeac95377b6a8c376f412dc4f'

def evaluate(d):
    ok, reason = prior.evaluate(d)
    if not ok:
        return False, reason
    if d['prs'][0]['parent_commit'] != FIRST_PARENT:
        return False, 'FIRST_PARENT_ANCHOR'
    if d['prs'][0]['merge_commit'] != FIRST_MERGE:
        return False, 'FIRST_MERGE_ANCHOR'
    return True, 'PASS_BOUNDARY_STRUCTURAL_ONLY'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('USAGE: guard manifest.json')
    try:
        with open(sys.argv[1],encoding='utf-8') as f:
            d=json.load(f)
        ok,reason=evaluate(d)
    except (OSError,ValueError,TypeError,RecursionError) as e:
        ok,reason=False,type(e).__name__
    print(json.dumps({'pass_test':ok,'reason':reason,'scope':'STRUCTURAL_ONLY'},sort_keys=True))
    sys.exit(0 if ok else 1)
