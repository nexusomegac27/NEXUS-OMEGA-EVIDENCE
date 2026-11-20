#!/usr/bin/env python3
"""R36 bounded synthetic falsification of the retained-causal-thread rule.

Proof of a property of this minimal test harness is NOT proof of the live
NEXUS graph, historical causal completeness, authentic device original or consent.
"""
from collections import deque
from dataclasses import dataclass
import unittest

EVIDENCE = 'EVIDENCE_BOUND'
REPORT = 'REPORTED_ONLY'
HYPOTHESIS = 'HYPOTHETICAL_BRIDGE'
GAP = 'UNKNOWN_LINK'
VERIFIED = 'SOURCE_VERIFIED'
UNKNOWN = 'NOT_IN_CUSTODY'
WITHHELD = 'ACCESS_RESTRICTED'
CONFLICT = 'CONFLICTED'

@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    kind: str


def bounded_path(nodes, edges, start, finish, *, evidential, limit=20):
    """Return reachability only; never infer a missing edge or validate a cause."""
    if start not in nodes or finish not in nodes:
        return False
    graph = {}
    for edge in edges:
        if edge.src not in nodes or edge.dst not in nodes:
            raise ValueError('DANGLING_SOURCE_OR_TARGET')
        if edge.kind not in {EVIDENCE, REPORT, HYPOTHESIS, GAP}:
            raise ValueError('UNKNOWN_EVIDENCE_KIND')
        if evidential and (edge.kind != EVIDENCE or
                           nodes[edge.src] != VERIFIED or nodes[edge.dst] != VERIFIED):
            continue
        graph.setdefault(edge.src, []).append(edge.dst)
    frontier = deque([start])
    visited = set()
    while frontier:
        if len(visited) >= limit:
            raise ValueError('SEARCH_BUDGET_EXHAUSTED')
        at = frontier.popleft()
        if at in visited:
            continue
        visited.add(at)
        if at == finish:
            return not evidential or nodes[at] == VERIFIED
        frontier.extend(x for x in graph.get(at, ()) if x not in visited)
    return False


def context_report(nodes, edges, source, target, limit=20):
    possible = bounded_path(nodes, edges, source, target, evidential=False, limit=limit)
    closed = bounded_path(nodes, edges, source, target, evidential=True, limit=limit)
    return {
        'context_route_known': possible,
        'evidence_chain_closed': closed,
        'unresolved_nodes': sorted(k for k, v in nodes.items() if v != VERIFIED),
        'unverified_edges': sorted((e.src, e.dst, e.kind) for e in edges if e.kind != EVIDENCE),
        'claim_promotion_allowed': False,
    }


class GapDoctrineFalsification(unittest.TestCase):
    def setUp(self):
        self.nodes = {'R35': VERIFIED, 'R36': VERIFIED, 'R21_original': UNKNOWN,
                      'device': UNKNOWN, 'transport': UNKNOWN}
        self.edges = [Edge('R35', 'R36', EVIDENCE),
                      Edge('R36', 'R21_original', GAP),
                      Edge('R21_original', 'device', HYPOTHESIS),
                      Edge('device', 'transport', REPORT)]

    def test_01_missing_keeps_context_not_proof(self):
        r = context_report(self.nodes, self.edges, 'R35', 'transport')
        self.assertTrue(r['context_route_known'])
        self.assertFalse(r['evidence_chain_closed'])
        self.assertFalse(r['claim_promotion_allowed'])

    def test_02_verified_prefix_remains_valid_only_to_r36(self):
        self.assertTrue(bounded_path(self.nodes, self.edges, 'R35', 'R36', evidential=True))
        self.assertFalse(bounded_path(self.nodes, self.edges, 'R35', 'device', evidential=True))

    def test_03_reported_is_not_original(self):
        nodes = dict(self.nodes, R21_original=REPORT)
        self.assertFalse(bounded_path(nodes, self.edges, 'R35', 'transport', evidential=True))

    def test_04_no_hallucinated_missing_node(self):
        bad = self.edges + [Edge('R21_original', 'not_supplied_file', EVIDENCE)]
        with self.assertRaisesRegex(ValueError, 'DANGLING'):
            context_report(self.nodes, bad, 'R35', 'transport')

    def test_05_conflict_not_resolved_by_reachability(self):
        nodes = dict(self.nodes, R21_original=CONFLICT)
        self.assertFalse(context_report(nodes, self.edges, 'R35', 'transport')['evidence_chain_closed'])

    def test_06_access_denied_not_conflated_with_absence(self):
        nodes = dict(self.nodes, R21_original=WITHHELD)
        self.assertIn('R21_original', context_report(nodes, self.edges, 'R35', 'transport')['unresolved_nodes'])
        self.assertNotEqual(WITHHELD, UNKNOWN)

    def test_07_hypothetical_link_cannot_be_witness(self):
        nodes = {k: VERIFIED for k in self.nodes}
        self.assertFalse(bounded_path(nodes, self.edges, 'R35', 'transport', evidential=True))

    def test_08_bounded_no_infinite_cycle(self):
        cyc = self.edges + [Edge('transport', 'R35', HYPOTHESIS)]
        with self.assertRaisesRegex(ValueError, 'SEARCH_BUDGET'):
            bounded_path(self.nodes, cyc, 'R35', 'transport', evidential=False, limit=2)

    def test_09_real_verified_path_is_allowed_as_graph_reachability_only(self):
        nodes = {k: VERIFIED for k in self.nodes}
        edges = [Edge(e.src, e.dst, EVIDENCE) for e in self.edges]
        self.assertTrue(bounded_path(nodes, edges, 'R35', 'transport', evidential=True))
        self.assertFalse(context_report(nodes, edges, 'R35', 'transport')['claim_promotion_allowed'])

    def test_10_removed_gap_does_not_automatically_replace_edge(self):
        edges = self.edges[:1] + self.edges[2:]
        self.assertFalse(bounded_path(self.nodes, edges, 'R35', 'transport', evidential=False))


if __name__ == '__main__':
    unittest.main(verbosity=2)
