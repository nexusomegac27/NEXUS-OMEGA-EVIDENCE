"""C1 research-only bounded handoff census guard; no GitHub/network writes.

Input is caller-supplied, NOT authenticated source bytes. Cohort figures are
structural illustrations; this code never attests to a project-wide 90% rate.
"""
import re

HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
GITHUB_RECEIPT = re.compile(r'https://github\.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/(?:issues|pull)/\d+(?:#issuecomment-\d+)?\Z')
FLAGS = {'YES', 'NO', 'UNKNOWN'}


def valid_hex(value, pattern):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def eligible(event):
    flags = [event[k] for k in ('public', 'routine', 'authorized', 'accessible')]
    if 'NO' in flags:
        return 'NO'
    if 'UNKNOWN' in flags:
        return 'UNKNOWN'
    return 'YES'


def structurally_supported_unattended(event):
    if event.get('unattended') != 'YES' or event.get('operator_nudge') != 'NO_VERIFIED':
        return False
    if not valid_hex(event.get('source_commit'), HEX40):
        return False
    if not valid_hex(event.get('source_sha256'), HEX64):
        return False
    if event.get('readback_sha256') != event.get('source_sha256'):
        return False
    if not isinstance(event.get('source_bytes'), int) or isinstance(event['source_bytes'], bool) or event['source_bytes'] <= 0:
        return False
    path = event.get('source_path')
    if not isinstance(path, str) or not path.startswith('research/') or '..' in path or len(path) > 240:
        return False
    return all(isinstance(event.get(k), str) and GITHUB_RECEIPT.fullmatch(event[k])
               for k in ('trigger_receipt', 'handoff_receipt', 'independent_evaluator_receipt'))


def assess(events, population):
    """Count only supplied, structurally supported, eligible handoffs.

    An unknown eligibility or incomplete census forces NOT_COMPUTABLE.
    The supplied receipt strings are NOT independently authenticated here.
    """
    out = {'status': 'INVALID_INPUT', 'numerator': None, 'denominator': None,
           'cohort_rate': None, 'project_rate': 'NOT_COMPUTABLE',
           'evidence_class': 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'}
    if not isinstance(events, list) or not 1 <= len(events) <= 1000:
        return out
    seen = set()
    for e in events:
        if not isinstance(e, dict) or not isinstance(e.get('id'), str) or not e['id'] or len(e['id']) > 128 or e['id'] in seen:
            return out
        seen.add(e['id'])
        if any(e.get(k) not in FLAGS for k in ('public', 'routine', 'authorized', 'accessible')):
            return out
    if not isinstance(population, dict):
        return out
    if not isinstance(population.get('scope'), str) or not population['scope'] or len(population['scope']) > 128:
        return out
    if (population.get('enumeration_complete') is not True
            or not valid_hex(population.get('enumeration_commit'), HEX40)
            or not valid_hex(population.get('enumeration_sha256'), HEX64)):
        out['status'] = 'NOT_COMPUTABLE'
        return out
    classifications = [eligible(e) for e in events]
    if 'UNKNOWN' in classifications:
        out['status'] = 'NOT_COMPUTABLE'
        return out
    denominator = classifications.count('YES')
    numerator = sum(1 for e, classification in zip(events, classifications)
                    if classification == 'YES' and structurally_supported_unattended(e))
    out.update(status='COHORT_DECLARED_ONLY', numerator=numerator, denominator=denominator,
               cohort_rate=(numerator / denominator if denominator else None))
    return out
