"""Public read-only NEXUS Agent Communication interface release checks.

Offline, standard-library-only. These tests validate a deploy candidate's static
public surface; they do not prove a Hostinger deployment or live agent runtime.
"""
from __future__ import annotations

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT / "research" / "communication" / "github-only-exchange-enforcement-20261029"
HTML = LANE / "NEXUS_AGENT_COMMUNICATION_PUBLIC_INTERFACE_V1.html"
STATUS = LANE / "NEXUS_AGENT_COMMUNICATION_PUBLIC_STATUS_V1.json"
PROTOCOL = LANE / "NEXUS_AGENT_COMMUNICATION_PUBLIC_PROTOCOL_V1.json"


class InterfaceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.hrefs = []
        self.lang = None
        self.script_count = 0
        self.form_count = 0

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])
        if tag == "script":
            self.script_count += 1
        if tag == "form":
            self.form_count += 1


class StaticInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw_html = HTML.read_text(encoding="utf-8")
        cls.status = json.loads(STATUS.read_text(encoding="utf-8"))
        cls.protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
        cls.document = InterfaceParser()
        cls.document.feed(cls.raw_html)
        cls.document.close()

    def test_doctype_and_language(self):
        self.assertTrue(self.raw_html.lower().startswith("<!doctype html>"))
        self.assertEqual(self.document.lang, "de")

    def test_no_script_and_no_form(self):
        self.assertEqual(self.document.script_count, 0)
        self.assertEqual(self.document.form_count, 0)

    def test_document_metadata_and_navigation(self):
        self.assertIn("main", self.document.tags)
        self.assertIn("nav", self.document.tags)
        self.assertIn("h1", self.document.tags)
        self.assertIn("meta name=\"viewport\"", self.raw_html)
        for anchor in ("#status", "#zugang", "#quellen", "#prinzipien"):
            self.assertIn(anchor, self.document.hrefs)

    def test_status_and_protocol_links_are_local(self):
        self.assertIn("status.json", self.document.hrefs)
        self.assertIn("protocol.json", self.document.hrefs)

    def test_existing_agent_border_is_reused(self):
        self.assertIn("https://www.nexus-mobile.de/ai/agent-border/", self.document.hrefs)
        self.assertIn("https://www.nexus-mobile.de/ai/agent-border/manifest.json", self.document.hrefs)

    def test_public_source_is_pinned(self):
        ref = self.status["public_source"]["current_audited_router_commit"]
        self.assertRegex(ref, r"^[a-f0-9]{40}$")
        self.assertIn(ref, self.raw_html)
        self.assertIn("/pull/185", self.raw_html)

    def test_public_status_is_not_false_live(self):
        self.assertEqual(self.status["interface_class"], "PUBLIC_READ_ONLY")
        self.assertEqual(self.status["public_external_write_api"], "OFF")
        self.assertIs(self.status["production_cutover_active"], False)
        self.assertEqual(self.status["external_authenticated_return"], "NOT_ESTABLISHED")
        self.assertNotEqual(self.status["release_state"], "WWW_LIVE_CONFIRMED")

    def test_protocol_uses_only_read_http_methods(self):
        allowed = self.protocol["http_methods"]
        self.assertEqual(allowed["GET"], "PUBLIC_READ")
        self.assertEqual(allowed["HEAD"], "PUBLIC_READ")
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            self.assertEqual(allowed[method], "OFF")

    def test_machine_contract_matches_claim_ceiling(self):
        self.assertEqual(self.status["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        self.assertEqual(self.protocol["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        self.assertEqual(self.status["transport_canonical"], self.protocol["canonical_transport"])
        self.assertEqual(self.protocol["independent_external_ack"], "NOT_ESTABLISHED")

    def test_unrestricted_provider_discovery(self):
        self.assertEqual(self.status["agent_provider_limit"], "NONE_BY_DESIGN")
        self.assertIs(self.status["account_required_for_public_read"], False)
        self.assertIs(self.protocol["public_read_account_required"], False)

    def test_public_document_retains_privacy_scope(self):
        self.assertEqual(self.status["privacy"]["public_feedback_form"], False)
        self.assertFalse(self.status["privacy"]["content_publication"] == "UNREVIEWED")
        self.assertIn("HOLD_UNSUPPORTED_PRIVATE", self.protocol["source_classes"])


if __name__ == "__main__":
    unittest.main()
