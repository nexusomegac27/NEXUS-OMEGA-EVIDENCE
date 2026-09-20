# Invariants + FIXTURE_LOOP_001. No live agent ranking.
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from loop_detector import detect_loop  # noqa: E402

FIX = json.loads((Path(__file__).resolve().parent / "FIXTURE_LOOP_001.json").read_text(encoding="utf-8"))
got = detect_loop(FIX["runs"])
assert got["new_evidence"] == "NO_NEW_EVIDENCE"
assert got["loop_risk"] == "DETECTED"
assert got["next"] == "NEW_METHOD_OR_HOLD"
assert got["independent_reproduction_index"] == 1
assert got["loop_index"] == 2

# EARQV: no global score
earqv = json.loads((Path(__file__).resolve().parent / "earqv.example.json").read_text(encoding="utf-8"))
assert earqv["global_score"] is None
assert earqv["leaderboard"] == "PROHIBITED"
assert "Q1_SOURCE_FIDELITY" in earqv["dimensions"]
assert len(earqv["dimensions"]) == 12

# Fundus holds not dropped
head = json.loads((ROOT / "research" / "fundus" / "NEXUS_FUNDUS_HEAD.json").read_text(encoding="utf-8"))
assert head["truth_authority"] == "NO"
assert head["hold_may_be_dropped"] is False
assert any(e["kind"] == "HOLD" for e in head["entries"])
assert any(e["kind"] == "NEGATIVE" for e in head["entries"])

# SIM01 receipt invariants
rep = json.loads((Path(__file__).resolve().parent / "SIM01_REEXECUTION_RECEIPT.json").read_text(encoding="utf-8"))
assert rep["claim_ceiling"] == "C1_DESCRIPTIVE_ONLY"
assert rep["empirical_ndvi"] == "NOT_COMPUTED"
assert rep["numeric_reproduction"] == "MATCH"
assert rep["gt1pct_bug_rule"] == "REJECTED"
assert abs(rep["A"]["mc_mean"] - 0.09787719903756917) < 1e-15
assert abs(rep["B"]["mc_mean"] - 0.0978613610004723) < 1e-15
assert rep["r3_full_atomic_closure"] == "NO"
print("PASS")
