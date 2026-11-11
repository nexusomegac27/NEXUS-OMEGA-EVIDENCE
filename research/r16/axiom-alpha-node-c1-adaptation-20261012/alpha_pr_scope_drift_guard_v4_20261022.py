#!/usr/bin/env python3
"""Research-only PR narrative-vs-API scope checker, V4 (Unicode path ambiguity).

Inputs must be independently retrieved from GitHub at an immutable ref. This
checker neither authenticates an API response nor approves a PR/merge/claim.
It checks only the narrative fields for which the supplied snapshot has data;
file *change kind* (e.g. 'added') and complete pagination are NOT verified here.
"""
import re
import unicodedata

HEX40 = re.compile(r'^[0-9a-f]{40}$')
BASE = re.compile(r'\bfrom pinned main ([0-9a-f]{40})\b')
HEAD = re.compile(r'\bto pinned head ([0-9a-f]{40})\b')
COMMITS = re.compile(r'\b(\d+) commits? ahead\b')
FILES = re.compile(r'\b(two|\d+) added Markdown files only\b', re.I)
EXACT_LANE = re.compile(r'\bonly under the existing (research/[a-zA-Z0-9_./-]+/) lane\b')
GENERIC_LANE = re.compile(r'\bonly under the existing research lane\b')


def _safe_repo_path(p):
    """GitHub POSIX relative file path, without aliasing/traversal ambiguity."""
    if not isinstance(p, str) or not p or p.startswith('/') or '\\' in p or '\x00' in p:
        return False
    if p.startswith('./') or p.startswith('~') or '://' in p or ':' in p:
        return False
    segments = p.split('/')
    return all(seg not in ('', '.', '..') and not any(
        unicodedata.category(c) in ('Cc', 'Cf', 'Cs') for c in seg
    ) for seg in segments)


def check_scope(snapshot):
    """Return MATCH, DRIFT, or INCOMPLETE; fail closed on unverified inputs."""
    if not isinstance(snapshot, dict):
        return {'status': 'INCOMPLETE', 'reasons': ['INVALID_SNAPSHOT']}
    body = snapshot.get('body')
    base = snapshot.get('base_sha')
    head = snapshot.get('head_sha')
    commits = snapshot.get('commits')
    files = snapshot.get('changed_files')
    filenames = snapshot.get('filenames')
    if (not isinstance(body, str) or not isinstance(base, str)
        or not isinstance(head, str) or not HEX40.fullmatch(base)
        or not HEX40.fullmatch(head) or type(commits) is not int
        or type(files) is not int or commits < 0 or files < 0
        or not isinstance(filenames, list)
        or not all(isinstance(p, str) for p in filenames)
        or len(filenames) != files):
        return {'status': 'INCOMPLETE', 'reasons': ['INVALID_OR_INCONSISTENT_API_FIELDS']}
    m_base = BASE.search(body)
    m_head = HEAD.search(body)
    m_commits = COMMITS.search(body)
    m_files = FILES.search(body)
    if not all((m_base, m_head, m_commits, m_files)):
        return {'status': 'INCOMPLETE', 'reasons': ['UNPARSEABLE_SCOPE_CLAIM']}
    exact_lanes = EXACT_LANE.findall(body)
    generic_lane = bool(GENERIC_LANE.search(body))
    if len(exact_lanes) > 1 or (exact_lanes and generic_lane):
        return {'status': 'INCOMPLETE', 'reasons': ['AMBIGUOUS_LANE_CLAIM']}
    lane = exact_lanes[0] if exact_lanes else 'research/' if generic_lane else None
    if lane is None or not _safe_repo_path(lane[:-1]):
        return {'status': 'INCOMPLETE', 'reasons': ['UNPARSEABLE_OR_INVALID_LANE']}
    expected_files = 2 if m_files.group(1).lower() == 'two' else int(m_files.group(1))
    reasons = []
    if m_base.group(1) != base:
        reasons.append('BASE_SHA_DRIFT')
    if m_head.group(1) != head:
        reasons.append('HEAD_SHA_DRIFT')
    if int(m_commits.group(1)) != commits:
        reasons.append('COMMIT_COUNT_DRIFT')
    if expected_files != files:
        reasons.append('FILE_COUNT_DRIFT')
    if any(not p.lower().endswith('.md') for p in filenames):
        reasons.append('FILE_TYPE_DRIFT')
    if any(not _safe_repo_path(p) for p in filenames):
        reasons.append('INVALID_REPOSITORY_PATH')
    if any(not p.startswith(lane) for p in filenames):
        reasons.append('FILE_PATH_SCOPE_DRIFT')
    if len({unicodedata.normalize('NFC', p).casefold() for p in filenames}) != len(filenames):
        reasons.append('DUPLICATE_OR_CASE_COLLIDING_PATH')
    return {'status': 'DRIFT' if reasons else 'MATCH', 'reasons': reasons}
