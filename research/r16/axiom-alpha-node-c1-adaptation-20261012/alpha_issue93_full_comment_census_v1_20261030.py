#!/usr/bin/env python3
"""Offline C1-only checker for an API-derived Issue #93 comment metadata snapshot.

Not a GitHub authentication, immutability, science or project-wide handoff proof.
"""
import json
import sys
from datetime import datetime, timezone

SOURCE = "nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93"
OWNER = "nexusomegac27"

class Reject(ValueError):
    pass

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Reject("DUPLICATE_JSON_KEY")
        result[key] = value
    return result

def require(condition, code):
    if not condition:
        raise Reject(code)

def utc(value):
    require(isinstance(value, str) and value.endswith("Z"), "BAD_TIMESTAMP")
    try:
        dt = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise Reject("BAD_TIMESTAMP") from exc
    require(dt.tzinfo == timezone.utc, "BAD_TIMESTAMP")
    return dt

def check(snapshot):
    require(type(snapshot) is dict, "ROOT_NOT_OBJECT")
    require(snapshot.get("schema_version") == "alpha_issue93_comment_census_v1", "BAD_SCHEMA")
    require(snapshot.get("source") == SOURCE, "SOURCE_MISMATCH")
    count = snapshot.get("declared_count")
    require(type(count) is int and 1 <= count <= 100000, "BAD_COUNT")
    pages = snapshot.get("page_sizes")
    require(type(pages) is list and bool(pages) and all(type(n) is int and 1 <= n <= 100 for n in pages), "BAD_PAGES")
    require(sum(pages) == count, "PAGE_COUNT_MISMATCH")
    comments = snapshot.get("comments")
    require(type(comments) is list and len(comments) == count, "POPULATION_INCOMPLETE")
    last_id, last_time = None, None
    links = 0
    for index, item in enumerate(comments):
        require(type(item) is dict, "BAD_ROW")
        cid = item.get("id")
        require(type(cid) is int and cid > 0, "BAD_COMMENT_ID")
        require(last_id is None or cid > last_id, "DUPLICATE_OR_UNSORTED_ID")
        require(item.get("author") == OWNER, "UNREGISTERED_ACTOR")
        created = utc(item.get("created_at"))
        updated = utc(item.get("updated_at"))
        require(updated == created, "EDITED_COMMENT_METADATA")
        require(last_time is None or created >= last_time, "UNSORTED_TIME")
        predecessor = item.get("predecessor_id")
        require(predecessor is None or (type(predecessor) is int and predecessor > 0), "BAD_PREDECESSOR")
        if predecessor is not None:
            require(index > 0 and predecessor == last_id, "BROKEN_PREDECESSOR")
            links += 1
        last_id, last_time = cid, created
    return {"status": "PASS_METADATA_CENSUS", "comments": count, "predecessor_links": links,
            "owner_metadata": count, "unedited_metadata": count, "source_authentication": "NOT_ESTABLISHED",
            "full_handoff_denominator": "NOT_COMPUTABLE"}

def main():
    try:
        data = json.load(sys.stdin, object_pairs_hook=unique_object)
        output = check(data)
        print(json.dumps(output, sort_keys=True))
    except (Reject, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(exc)}, sort_keys=True))
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
