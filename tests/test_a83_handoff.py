import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_a83_handoff import validate_envelope
from a83_decision import decision_function

BASE=json.loads((ROOT/'examples/a83/handoff-envelope-v1.example.json').read_text())

def test_valid_envelope_structure():
    assert validate_envelope(dict(BASE)) == []
    assert decision_function([]) == 'C1.1_ARTIFACT_VALIDATED_STRUCTURE_ONLY'

def test_fixture_corpus_fail_closed():
    count=0
    for line in (ROOT/'validation/a83-handoff-negative-fixtures-v1.jsonl').read_text().splitlines():
        if not line.strip(): continue
        fx=json.loads(line); env=dict(BASE); env.update(fx.get('mutation',{})); errs=validate_envelope(env,fx.get('payload'))
        assert fx['expected_error'] in errs, (fx['id'],fx['expected_error'],errs)
        assert decision_function(errs)=='C1.2_CLOSED'
        count+=1
    assert count >= 16

def test_parent_must_exist_when_repository_root_is_supplied(tmp_path):
    env=dict(BASE)
    errs=validate_envelope(env,root=tmp_path)
    assert 'A83_PARENT_NOT_IN_LEDGER' in errs
