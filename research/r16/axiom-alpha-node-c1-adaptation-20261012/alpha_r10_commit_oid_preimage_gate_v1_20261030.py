#!/usr/bin/env python3
"""C1-only isolated research: bounded Git commit SHA-1 preimage search on normalized GitHub API metadata.

A matching Git object ID does NOT prove original Git bytes, API authenticity, actor identity or scientific claims.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

SHA40 = re.compile(r"[0-9a-f]{40}\Z")

def no_duplicates(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError("duplicate JSON key")
        obj[k] = v
    return obj

def reject_constant(_):
    raise ValueError("nonfinite JSON")

def exact(obj, keys):
    if not isinstance(obj, dict) or set(obj) != set(keys):
        raise ValueError("missing or unexpected fields")

def sha(x):
    if not isinstance(x, str) or not SHA40.fullmatch(x):
        raise ValueError("invalid Git SHA-1")
    return x

def identity(obj):
    exact(obj, ("name", "email", "date"))
    name, email, date = (obj[k] for k in ("name", "email", "date"))
    if not isinstance(name, str) or not isinstance(email, str) or not name or not email:
        raise ValueError("invalid identity")
    for x in (name, email):
        if any(c in x for c in ("\n", "\r", "\0", "<", ">")):
            raise ValueError("unsafe identity")
    if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", date):
        raise ValueError("date must be exact normalized UTC format")
    timestamp = int(dt.datetime.fromisoformat(date.replace("Z", "+00:00")).timestamp())
    return name, email, timestamp

def offsets():
    # Deliberately bounded timezone hypothesis set, not a proof of original timezone.
    for minutes in range(-12 * 60, 14 * 60 + 1, 15):
        sign = "+" if minutes >= 0 else "-"
        absolute = abs(minutes)
        yield f"{sign}{absolute // 60:02d}{absolute % 60:02d}"

def verify(o, pinned_commit):
    exact(o, ("commit_sha", "tree_sha", "parents", "author", "committer", "message", "api_signature_state"))
    if sha(o["commit_sha"]) != sha(pinned_commit):
        raise ValueError("commit pin mismatch")
    tree = sha(o["tree_sha"])
    parents = o["parents"]
    if not isinstance(parents, list) or len(parents) != 1:
        raise ValueError("expected one parent")
    parent = sha(parents[0])
    if o["api_signature_state"] != "unsigned":
        raise ValueError("unsupported signature state")
    message = o["message"]
    if not isinstance(message, str) or not message or "\0" in message or len(message.encode("utf-8")) > 4096:
        raise ValueError("invalid message")
    author = identity(o["author"])
    committer = identity(o["committer"])
    matches = []
    # GitHub API normalizes author and committer date to UTC, discarding original timezone.
    # Try a documented bounded hypothesis set, with identical author and committer offset.
    for tz in offsets():
        lines = [f"tree {tree}", f"parent {parent}",
                 f"author {author[0]} <{author[1]}> {author[2]} {tz}",
                 f"committer {committer[0]} <{committer[1]}> {committer[2]} {tz}"]
        payload = ("\n".join(lines) + "\n\n" + message).encode("utf-8")
        full = b"commit " + str(len(payload)).encode("ascii") + b"\0" + payload
        if hashlib.sha1(full).hexdigest() == pinned_commit:
            matches.append((tz, len(payload)))
    if len(matches) != 1:
        raise ValueError(f"preimage hypothesis matches: {len(matches)}")
    return {"status": "API_COMMIT_SHA1_PREIMAGE_MATCH_NOT_AUTHENTICATED",
            "commit_sha1": pinned_commit, "tree_sha1": tree,
            "parent_sha1": parent, "matching_timezone_hypothesis": matches[0][0],
            "reconstructed_commit_payload_bytes": matches[0][1],
            "original_raw_commit_bytes_obtained": False,
            "independent_receiver_ack": False,
            "actor_authenticated": False,
            "scientific_adjudication": False}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("projection")
    ap.add_argument("--commit", required=True)
    a = ap.parse_args()
    try:
        raw = Path(a.projection).read_bytes()
        if len(raw) > 32768:
            raise ValueError("oversize projection")
        o = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates, parse_constant=reject_constant)
        print(json.dumps(verify(o, a.commit), sort_keys=True))
        return 0
    except (ValueError, TypeError, UnicodeError, OSError) as e:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(e)}, sort_keys=True))
        return 2

if __name__ == "__main__":
    sys.exit(main())
