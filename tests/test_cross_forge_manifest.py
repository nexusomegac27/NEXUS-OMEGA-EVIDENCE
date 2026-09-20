import json
import re
from pathlib import Path


def load():
    return json.loads(Path("cross_forge/manifest.json").read_text(encoding="utf-8"))


def test_sha256_is_canonical_content_digest():
    d = load()
    assert d["canonical_content_digest"] == "SHA256"
    assert re.fullmatch(r"[0-9a-f]{64}", d["terminal_bundle"]["master_sha256"])


def test_no_implicit_promotion_or_mutation_authority():
    d = load()
    assert d["claim_ceiling"] == "C1"
    assert d["merge"] is False
    assert d["deploy"] is False
    assert d["claim_promotion"] is False
    assert d["source_object_substitution"] is False


def test_gitlab_starts_as_independent_foundation_not_verified_mirror():
    d = load()
    assert d["gitlab"]["role"] == "INDEPENDENT_SECONDARY_FORGE"
    assert d["cross_forge_state"] == "FOUNDATION_ONLY_REPLICATION_NOT_YET_ESTABLISHED"


def test_terminal_bundle_not_overclaimed():
    d = load()
    assert d["terminal_bundle"]["axiom_independent_rehash"] == "NOT_EXECUTED_SOURCE_BYTES_NOT_PRESENT"
