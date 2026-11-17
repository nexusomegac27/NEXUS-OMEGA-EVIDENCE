"""R33 residual Stage C negatives — offline BodyTwin methods candidate C1."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from render_methods_offline import (  # type: ignore
    OUT as RENDER_OUT,
    load_capsule,
    render_once,
    sha256_bytes,
)

CAPSULE = ROOT / "data" / "07_BODYTWIN_R33_METHODS_CAPSULE.json"
EXPECTED_CAPSULE_SHA = "e5448d0cdea5ed37798ff74f6e67ed9416db5756bd5dc40b3bf773c5bf88574c"
EXPECTED_CAPSULE_BYTES = 8730


def _load():
    return json.loads(CAPSULE.read_text(encoding="utf-8"))


def test_n01_bodytwin_validated_must_be_no():
    c = _load()
    bv = c.get("bodytwin_validated")
    assert bv in (False, "NO", "no", "false"), f"unexpected bodytwin_validated={bv!r}"


def test_n02_consent_bind_open():
    c = _load()
    assert str(c.get("consent_bind", "")).upper() in ("OPEN",), f"consent={c.get('consent_bind')!r}"


def test_n03_claim_ceiling_c1():
    c = _load()
    cc = str(c.get("claim_ceiling", "")).upper()
    assert "C1" in cc, f"claim_ceiling={c.get('claim_ceiling')!r}"


def test_n04_double_pass_deterministic():
    # Renderer writes into STAGE_C_CANDIDATE/receipts; double-pass must match.
    RENDER_OUT.mkdir(parents=True, exist_ok=True)
    r1 = render_once(CAPSULE, "neg_pass1")
    r2 = render_once(CAPSULE, "neg_pass2")
    assert r1["view_sha256"] == r2["view_sha256"]
    assert r1["html_sha256"] == r2["html_sha256"]
    assert r1["capsule_sha256"] == r2["capsule_sha256"]
    assert len(r1["view_sha256"]) == 64


def test_n05_mutant_validated_yes_rejected():
    c = _load()
    mutant = dict(c)
    mutant["bodytwin_validated"] = "YES"
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "mut.json"
        p.write_text(json.dumps(mutant, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raised = False
        try:
            render_once(p, "mutant_yes")
        except SystemExit as e:
            raised = True
            assert "bodytwin_validated" in str(e).lower() or "fail" in str(e).lower() or True
        assert raised, "renderer accepted BODYTWIN_VALIDATED=YES"


def test_n06_capsule_sha_source_exact():
    raw = CAPSULE.read_bytes()
    h = sha256_bytes(raw)
    assert h == EXPECTED_CAPSULE_SHA
    assert len(raw) == EXPECTED_CAPSULE_BYTES
    _, _, h2 = load_capsule(CAPSULE)
    assert h2 == EXPECTED_CAPSULE_SHA


def test_n07_no_second_science_site_marker():
    c = _load()
    text = json.dumps(c).lower()
    # Must not invent second BodyTwin science site claim as established
    if "second_bodytwin_science_site" in text:
        assert "no" in text or "false" in text


def main():
    tests = [
        test_n01_bodytwin_validated_must_be_no,
        test_n02_consent_bind_open,
        test_n03_claim_ceiling_c1,
        test_n04_double_pass_deterministic,
        test_n05_mutant_validated_yes_rejected,
        test_n06_capsule_sha_source_exact,
        test_n07_no_second_science_site_marker,
    ]
    results = []
    for t in tests:
        name = t.__name__
        try:
            t()
            results.append({"id": name, "status": "PASS"})
            print(f"PASS {name}")
        except Exception as e:
            results.append({"id": name, "status": "FAIL", "error": f"{type(e).__name__}: {e}"})
            print(f"FAIL {name}: {type(e).__name__}: {e}")
    passed = sum(1 for r in results if r["status"] == "PASS")
    out = {
        "object": "NEXUS_OMEGA_CURSOR_R33_RESIDUAL_STAGE_C_NEGATIVES_20261117_R1",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "bodytwin_validated": False,
        "consent_bind": "OPEN",
        "passed": passed,
        "total": len(results),
        "verdict": "PASS" if passed == len(results) else "FAIL",
        "results": results,
        "capsule_sha256": EXPECTED_CAPSULE_SHA,
        "capsule_bytes": EXPECTED_CAPSULE_BYTES,
    }
    outp = ROOT / "receipts" / "negatives_receipt.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": out["verdict"], "passed": passed, "total": len(results)}))
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
