# NEXUS OMEGA — QWEN-CODER R5 START HERE

```text
OBJECT = NEXUS_OMEGA_QWEN_CODER_R5_GITHUB_DELIVERY_START_20260831_R0
STATE = GITHUB_NATIVE_TRANSPORT_ESTABLISHED_PENDING_RECEIVER_REHASH
FROM = OPERATOR_ALEXANDER_VIA_AXIOM
TO = QWEN-CODER
CLAIM = C1_DESCRIPTIVE_ONLY
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
PUBLIC_WRITE_BY_QWEN = NO
```

## 1. Authoritative transport object

The canonical R5 start package was originally created as:

`NEXUS_OMEGA_QWEN_CODER_R5_MAXIMUM_PROGRESS_TRANSPORT_20260831_R0.zip`

Expected identity:

```text
BYTES = 26395
SHA256 = 9a8c2882d8fe8bda6021256ee4e351755b637761ab651bdbd480fe1955303331
```

GitHub transport cannot directly preserve this binary ZIP through the current connector, therefore the exact ZIP bytes are exposed here as six RFC-4648 Base64 chunks under:

`research/r5/qwen-coder-start/transport/`

The chunk identities are bound by `TRANSPORT_MANIFEST.json`.

## 2. Mandatory receiver procedure

Do not begin semantic work before reconstructing and verifying the package.

From the repository checkout on branch:

`axiom/r5-qwen-coder-start-20260831`

run conceptually:

```bash
cat research/r5/qwen-coder-start/transport/r5_qwen_transport.part01.b64 \
    research/r5/qwen-coder-start/transport/r5_qwen_transport.part02.b64 \
    research/r5/qwen-coder-start/transport/r5_qwen_transport.part03.b64 \
    research/r5/qwen-coder-start/transport/r5_qwen_transport.part04.b64 \
    research/r5/qwen-coder-start/transport/r5_qwen_transport.part05.b64 \
    research/r5/qwen-coder-start/transport/r5_qwen_transport.part06.b64 \
  | base64 -d > NEXUS_OMEGA_QWEN_CODER_R5_MAXIMUM_PROGRESS_TRANSPORT_20260831_R0.zip

wc -c NEXUS_OMEGA_QWEN_CODER_R5_MAXIMUM_PROGRESS_TRANSPORT_20260831_R0.zip
sha256sum NEXUS_OMEGA_QWEN_CODER_R5_MAXIMUM_PROGRESS_TRANSPORT_20260831_R0.zip
```

Required result:

```text
BYTES = 26395
SHA256 = 9a8c2882d8fe8bda6021256ee4e351755b637761ab651bdbd480fe1955303331
```

Then verify ZIP integrity and inspect the four contained canonical text objects.

If any chunk hash, reassembled byte count, reassembled SHA-256, ZIP integrity, or contained-object binding differs:

```text
STATE = HARD_FAIL_R5_GITHUB_TRANSPORT_BIND_MISMATCH_C1
STOP_SEMANTIC_USE = YES
```

Do not reconstruct, normalize, edit, or substitute.

## 3. Contained authoritative objects

The ZIP contains:

1. `NEXUS_OMEGA_QWEN_CODER_R5_MAXIMUM_PROGRESS_END_TO_END_ORDER_20260831_R0.md`
   - BYTES `27944`
   - SHA256 `15d9d3f2016f50d383f40d2b8fdfe1d3e6b6b6e48e8816ee54680d89c43e162d`

2. `NEXUS_OMEGA_QWEN_CODER_R5_MAXIMUM_PROGRESS_ORDER_RECEIPT_20260831_R0.json`
   - BYTES `938`
   - SHA256 `df7ca28105c1bf25883bfcc55cc9b4ffab38c5ada8cea3317033d82f44027427`

3. `NEXUS_OMEGA_GITHUB_FRAMEWORK_R4_CLOSURE_R5_CANONICAL_FOUNDATION_20260831_R0.md`
   - BYTES `35019`
   - SHA256 `fa319c72c93185a3d40f091f74f96b98098a059d61bb17f80a019a273182e317`

4. `NEXUS_OMEGA_GITHUB_FRAMEWORK_R4_CLOSURE_R5_CANONICAL_FOUNDATION_RECEIPT_20260831_R0.json`
   - BYTES `1084`
   - SHA256 `c5ca69d48593b46b70af64ef1398157820dbfde484958cf8a3348177e779c355`

## 4. Frozen public source baseline

The order expects the research baseline:

```text
REPOSITORY = nexusomegac27/NEXUS-OMEGA-EVIDENCE
EXPECTED_MAIN = bc312c4d2cd6afa579db1f077c88d8fe08fc9470
EXPECTED_TREE = c8856faa74efa5770717d2d44dc7d51e4269cb22
EXPECTED_PARENT = bb1f3fd88db79d295077062895574c6d90b390bf
```

Independently retrieve the live state. If main has drifted, do not silently rebase the frozen R5 foundation. Record both states and continue frozen-base work where lawful.

## 5. QWEN-CODER operating boundary

Your role is maximum-progress R5 research, formalization, local candidate implementation and falsification.

You are explicitly NOT authorized by this delivery to:

```text
git push
create PR
merge
mutate main
mutate Rulesets
create release/tag
publish attestations
claim promotion
foundation promotion
```

`BLOCKED_LANE != BLOCKED_SYSTEM` and work-conserving execution are mandatory.

Do not attempt to confirm R4. Attempt to break the R5 foundation, formalize surviving concepts, create executable validators/tests/fixtures, and return physically persisted byte-bound outputs exactly as required by the contained order.

## 6. Return route

Your terminal result must return to AXIOM for independent rehash and R5 adjudication. Any implementation produced by you remains producer output until a separate independent validator has inspected the actual bytes.
