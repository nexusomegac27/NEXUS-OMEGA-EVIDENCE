#!/usr/bin/env python3
"""NEXUS Anchor V1.2 – file-exact signed online handoff reference (C1 sandbox candidate).

This does not grant execution authorization; it cannot replace access to payload bytes.
Requires cryptography for Ed25519. Never create/ship a real operator private key here.
"""
from __future__ import annotations

import argparse
import base64
import binascii
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlparse
import ipaddress
import unicodedata
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

SCHEMA = "NEXUS_HANDOFF_V1_2"
DOMAIN = b"NEXUS_OMEGA_HANDOFF_MANIFEST_V1_2\0"
CEILING = "C1_DESCRIPTIVE_ONLY"
OBJECT_PATTERN = re.compile(r"^NEXUS_[A-Z0-9_]{6,180}$")
HEXDIGEST = re.compile(r"^[0-9a-f]{64}$")
TOP_KEYS = {"schema", "object", "lane", "sequence", "previous_manifest_sha256", "issued_at", "claim_ceiling", "classification", "payload", "signature"}
PAYLOAD_KEYS = {"filename", "bytes", "sha256", "url"}
SIG_KEYS = {"algorithm", "public_key_spki_sha256", "base64"}
CLASSIFICATIONS = {"PUBLIC_SAFE", "PRIVATE_ENCRYPTED", "PRIVATE_WITNESS_ONLY"}


class HandshakeError(Exception):
    pass


# V1.2: syntax guard only. Network fetcher MUST separately enforce trusted
# host allowlists, resolved-IP egress policy, redirects and DNS rebinding.
def validate_shared_host(host: str):
    if not host or host.endswith('.') or '%' in host or '\x00' in host:
        raise HandshakeError('noncanonical or empty URL host')
    h = host.lower()
    if h in {'localhost', 'localhost.localdomain'} or h.endswith(('.local', '.localhost', '.internal', '.intranet')):
        raise HandshakeError('local/internal hostname denied')
    try:
        addr=ipaddress.ip_address(h)
    except ValueError:
        # Numeric IPv4 aliases in decimal/octal/hex/short-dot notation are
        # parsed as loopback by some downstream clients (SSRF).
        labels=h.split('.')
        if len(labels)==1: raise HandshakeError('single-label hostname denied')
        numeric=lambda x: x.isdecimal() or (x.startswith('0x') and len(x)>2 and all(c in '0123456789abcdef' for c in x[2:]))
        if all(numeric(l) for l in labels): raise HandshakeError('ambiguous numeric hostname denied')
        if any(not l or not re.fullmatch(r'[a-z0-9-]+',l) or l.startswith('-') or l.endswith('-') for l in labels):
            raise HandshakeError('invalid hostname label')
    else:
        if not addr.is_global: raise HandshakeError('non-public IP denied')


def validate_safe_filename(name: str):
    if not name or name in ('.','..') or len(name)>160 or '/' in name or '\\' in name or ':' in name or name.rstrip(' .')!=name:
        raise HandshakeError('non-portable payload filename')
    if any(unicodedata.category(c).startswith('C') for c in name):
        raise HandshakeError('control or bidi filename prohibited')
    stem=name.split('.')[0].upper()
    if stem in {'CON','PRN','AUX','NUL'} or re.fullmatch(r'(COM|LPT)[1-9]',stem):
        raise HandshakeError('reserved Windows payload filename')


def canonical(value):
    """NEXUS_CJSON1: integer-only JSON, ASCII field names, sorted Python key order.
    Explicitly NOT claimed to implement RFC 8785 (JCS)."""
    def check(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if not isinstance(k, str) or not k.isascii():
                    raise HandshakeError("non-ASCII JSON field name")
                check(v)
        elif isinstance(x, list):
            for v in x: check(v)
        elif isinstance(x, bool) or x is None or isinstance(x, str):
            if isinstance(x, str): x.encode('utf-8', 'strict')
        elif isinstance(x, int) and not isinstance(x, bool):
            if x < -(2**53-1) or x > 2**53-1:
                raise HandshakeError("unsafe JSON integer range")
        else:
            raise HandshakeError("float/invalid JSON type forbidden")
    check(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')


def object_no_duplicates(pairs):
    x = {}
    for k, v in pairs:
        if k in x:
            raise HandshakeError("duplicate JSON field: " + k)
        x[k] = v
    return x


def read_json(p):
    path = Path(p)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 524288:
        raise HandshakeError("invalid/oversized manifest or state")
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=object_no_duplicates)
    except (UnicodeError, json.JSONDecodeError) as e:
        raise HandshakeError("malformed JSON: " + str(e)) from e


def file_info(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file():
        raise HandshakeError("payload must be one real, regular file; no directories or symlinks")
    stat1 = p.stat()
    h = hashlib.sha256()
    with p.open('rb') as fd:
        for block in iter(lambda: fd.read(2**18), b''):
            h.update(block)
    stat2 = p.stat()
    if (stat1.st_ino, stat1.st_size, stat1.st_mtime_ns) != (stat2.st_ino, stat2.st_size, stat2.st_mtime_ns):
        raise HandshakeError("payload changed while hashing")
    if stat2.st_size == 0:
        raise HandshakeError("empty payload prohibited")
    return stat2.st_size, h.hexdigest()


def spki_hash(pub):
    der = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return hashlib.sha256(der).hexdigest()


def signed_bytes(manifest):
    unsigned = dict(manifest)
    unsigned.pop('signature', None)
    return DOMAIN + canonical(unsigned)


def manifest_hash(manifest):
    return hashlib.sha256(canonical(manifest)).hexdigest()


def check_schema(m):
    if not isinstance(m, dict) or set(m) != TOP_KEYS: raise HandshakeError("unknown or missing manifest fields")
    if m['schema'] != SCHEMA or m['claim_ceiling'] != CEILING: raise HandshakeError("schema or claim ceiling invalid")
    if not isinstance(m['object'], str) or not OBJECT_PATTERN.fullmatch(m['object']): raise HandshakeError("object invalid")
    if not isinstance(m['lane'], str) or not re.fullmatch(r"[A-Za-z0-9_:-]{1,96}", m['lane']): raise HandshakeError("lane invalid")
    if type(m['sequence']) is not int or not 1 <= m['sequence'] <= 2**31-1: raise HandshakeError("sequence invalid")
    prev = m['previous_manifest_sha256']
    if prev is not None and (not isinstance(prev, str) or not HEXDIGEST.fullmatch(prev)):
        raise HandshakeError("previous hash invalid")
    if m['sequence'] == 1 and prev is not None: raise HandshakeError("genesis prev must be null")
    try:
        dt = datetime.strptime(m['issued_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    except (ValueError, TypeError) as e: raise HandshakeError("issued_at invalid") from e
    if dt.year < 2025: raise HandshakeError("issued_at unexpectedly old")
    if (dt - datetime.now(timezone.utc)).total_seconds() > 600: raise HandshakeError('issued_at more than 10min in future')
    if m['classification'] not in CLASSIFICATIONS: raise HandshakeError("classification invalid")
    if m['classification'] == 'PRIVATE_ENCRYPTED':
        raise HandshakeError("PRIVATE_ENCRYPTED not yet implemented: .age extension is not encryption proof")
    p = m['payload']
    if not isinstance(p, dict) or set(p) != PAYLOAD_KEYS: raise HandshakeError("payload schema invalid")
    if not isinstance(p['filename'], str) or not (1 <= len(p['filename']) <= 160) or p['filename'] in ('.','..') or '/' in p['filename'] or '\\' in p['filename']:
        raise HandshakeError("payload filename invalid")
    validate_safe_filename(p['filename'])
    if type(p['bytes']) is not int or p['bytes'] <= 0: raise HandshakeError("payload size invalid")
    if not isinstance(p['sha256'], str) or not HEXDIGEST.fullmatch(p['sha256']): raise HandshakeError("payload hash invalid")
    url = p['url']
    if url is not None:
        if not isinstance(url, str) or len(url) > 2048:
            raise HandshakeError("payload locator must be HTTPS")
        parsed = urlparse(url)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise HandshakeError("URL must be HTTPS without inline credentials, query tokens or fragments")
        validate_shared_host(parsed.hostname)
        try:
            _ = parsed.port
        except ValueError as e: raise HandshakeError('invalid URL port') from e
    if m['classification'] == 'PUBLIC_SAFE' and url is None:
        raise HandshakeError("PUBLIC_SAFE needs a real downloadable URL")
    if m['classification'] == 'PRIVATE_ENCRYPTED' and url is None:
        raise HandshakeError("PRIVATE_ENCRYPTED needs a ciphertext download URL")
    if m['classification'] == 'PRIVATE_WITNESS_ONLY' and url is not None:
        raise HandshakeError("witness-only cannot pretend to deliver bytes")
    s = m['signature']
    if not isinstance(s, dict) or set(s) != SIG_KEYS or s['algorithm'] != 'Ed25519':
        raise HandshakeError("signature structure invalid")
    if not isinstance(s['public_key_spki_sha256'], str) or not HEXDIGEST.fullmatch(s['public_key_spki_sha256']):
        raise HandshakeError("key fingerprint invalid")
    if not isinstance(s['base64'], str): raise HandshakeError("signature encoding invalid")
    try:
        sig=base64.b64decode(s['base64'],validate=True)
    except (binascii.Error,ValueError) as e:
        raise HandshakeError('signature base64 invalid') from e
    if len(sig)!=64 or base64.b64encode(sig).decode('ascii') != s['base64']:
        raise HandshakeError('noncanonical Ed25519 signature encoding')
    canonical(m)


def read_private(path):
    if Path(path).is_symlink(): raise HandshakeError("private key symlink rejected")
    return serialization.load_pem_private_key(Path(path).read_bytes(), password=None)


def sign(manifest, key):
    s = dict(manifest)
    s['signature'] = {"algorithm":"Ed25519", "public_key_spki_sha256":spki_hash(key.public_key()), "base64":base64.b64encode(key.sign(signed_bytes(s))).decode('ascii')}
    check_schema(s)
    return s


def signature_verify(m, trusted_pub_file, pinned_fp):
    pub = serialization.load_pem_public_key(Path(trusted_pub_file).read_bytes())
    actual_fp = spki_hash(pub)
    if not HEXDIGEST.fullmatch(pinned_fp) or actual_fp != pinned_fp:
        raise HandshakeError("public key is NOT pinned by trusted out-of-band fingerprint")
    if actual_fp != m['signature']['public_key_spki_sha256']:
        raise HandshakeError("manifest signer not allowlisted")
    try:
        sig = base64.b64decode(m['signature']['base64'], validate=True)
        pub.verify(sig, signed_bytes(m))
    except (binascii.Error, InvalidSignature, ValueError) as e:
        raise HandshakeError("invalid signature") from e


def file_atomic_write(path, data):
    p=Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=str(p.parent), prefix='.nxo-write-')
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(temp, p)
    finally:
        if os.path.exists(temp): os.remove(temp)


def make(args):
    size, digest = file_info(args.payload)
    if args.classification == 'PRIVATE_ENCRYPTED':
        raise HandshakeError("PRIVATE_ENCRYPTED is reserved for a later audited age encrypt/decrypt adapter")
    if args.classification == 'PRIVATE_WITNESS_ONLY' and args.url:
        raise HandshakeError("witness only cannot have URL")
    if args.classification != 'PRIVATE_WITNESS_ONLY' and not args.url:
        raise HandshakeError("real payload delivery URL required")
    obj = {
        "schema":SCHEMA,"object":args.object,"lane":args.lane,
        "sequence":args.sequence,"previous_manifest_sha256":args.prev_hash,
        "issued_at":datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "claim_ceiling":CEILING,"classification":args.classification,
        "payload":{"filename":Path(args.payload).name,"bytes":size,"sha256":digest,"url":args.url},
    }
    k = read_private(args.sign_key)
    m = sign(obj,k)
    file_atomic_write(args.output,(json.dumps(m,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('MANIFEST_SHA256='+manifest_hash(m))
    print('PAYLOAD_SHA256='+digest)
    print('COPY_PASTE=OBJECT '+args.object+' | MANIFEST_SHA256 '+manifest_hash(m)+' | PAYLOAD_URL '+str(args.url)+' | CLAIM C1')
    print('PUBLISHED=NO (manifest creation never implies publication or ACK)')


def verify(args):
    m=read_json(args.manifest)
    check_schema(m)
    signature_verify(m,args.pubkey,args.pinned_key_sha256)
    size,digest=(None,None)
    if args.payload:
        size,digest=file_info(args.payload)
        if Path(args.payload).name != m['payload']['filename']:
            raise HandshakeError('payload filename differs from signed manifest')
        if (size,digest)!=(m['payload']['bytes'],m['payload']['sha256']):
            raise HandshakeError("received PAYLOAD BYTES do not match signed manifest")
    elif not args.witness_only:
        raise HandshakeError("NO_PAYLOAD: only witness-only inspection possible, never ACK")
    if m['classification']=='PRIVATE_WITNESS_ONLY' and args.record:
        raise HandshakeError("witness-only never qualifies as delivery ACK")
    h=manifest_hash(m)
    if args.witness_only:
        if args.record: raise HandshakeError("witness cannot record an ACK")
        print('STATE=SIGNED_WITNESS_ONLY_NO_PAYLOAD_NO_RECEIPT')
        print('MANIFEST_SHA256='+h)
        return
    if not args.payload: raise HandshakeError("verified signature alone is not delivery")
    if not args.state_file:
        print('STATE=PAYLOAD_AND_SIGNATURE_VALID_REPLAY_UNCHECKED_NO_ACK')
        print('MANIFEST_SHA256='+h)
        if args.record: raise HandshakeError("record requires replay state")
        return
    if os.name == 'nt':
        raise HandshakeError('REPLAY_STATE_LOCK_UNAVAILABLE_ON_WINDOWS: use authorized Linux broker')
    try:
        import fcntl  # POSIX lock only; FS ACL/remote receipt remain mandatory.
    except ImportError as e:
        raise HandshakeError('REPLAY_STATE_LOCK_NOT_SUPPORTED_ON_PLATFORM') from e
    state=Path(args.state_file)
    lock=state.with_suffix(state.suffix+'.lock')
    state.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a+b') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        prev = read_json(state) if state.exists() else None
        if prev is None:
            if m['sequence']!=1 or m['previous_manifest_sha256'] is not None:
                raise HandshakeError("genesis mismatch")
        else:
            if prev.get('lane')!=m['lane'] or prev.get('object')!=m['object']:
                raise HandshakeError("state binding mismatch")
            if prev.get('sequence')==m['sequence'] and prev.get('manifest_sha256')==h:
                print('STATE=ALREADY_VERIFIED_IDEMPOTENT_NOT_NEW_EXECUTION')
                return
            if m['sequence']!=prev.get('sequence',0)+1 or m['previous_manifest_sha256']!=prev.get('manifest_sha256'):
                raise HandshakeError("REPLAY_OR_CHAIN_MISMATCH")
        if args.record:
            file_atomic_write(state,canonical({'lane':m['lane'],'object':m['object'],'sequence':m['sequence'],'manifest_sha256':h}))
            print('STATE=CONTENT_SIGNATURE_AND_CHAIN_MATCH_RECEIPT_RECORD_REQUIRES_SEPARATE_ACTOR_AUTH')
        else:
            print('STATE=CONTENT_SIGNATURE_AND_CHAIN_VALID_NOT_RECORDED')
        print('MANIFEST_SHA256='+h)


def main():
    p=argparse.ArgumentParser(description='NEXUS Anchor V1.2 C1 research reference (NOT an identity authority)')
    sub=p.add_subparsers(dest='cmd',required=True)
    m=sub.add_parser('make')
    m.add_argument('--payload',required=True)
    m.add_argument('--object',required=True)
    m.add_argument('--lane',required=True)
    m.add_argument('--classification',choices=sorted(CLASSIFICATIONS),required=True)
    m.add_argument('--url')
    m.add_argument('--sequence',type=int,default=1)
    m.add_argument('--prev-hash')
    m.add_argument('--sign-key',required=True)
    m.add_argument('--output',required=True)
    m.set_defaults(func=make)
    v=sub.add_parser('verify')
    v.add_argument('--manifest',required=True)
    v.add_argument('--pubkey',required=True)
    v.add_argument('--pinned-key-sha256',required=True)
    v.add_argument('--payload')
    v.add_argument('--state-file')
    v.add_argument('--record',action='store_true')
    v.add_argument('--witness-only',action='store_true')
    v.set_defaults(func=verify)
    a=p.parse_args()
    try:a.func(a)
    except (HandshakeError,OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        print('FAIL_CLOSED: '+str(e),file=sys.stderr)
        return 2
    return 0

if __name__=='__main__':sys.exit(main())
