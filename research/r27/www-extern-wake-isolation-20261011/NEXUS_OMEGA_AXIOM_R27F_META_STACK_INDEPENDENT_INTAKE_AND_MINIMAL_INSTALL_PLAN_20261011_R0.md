# NEXUS OMEGA · AXIOM R27-F META-LABELED SOURCE AUDIT / minimaler Installationsanschluss
## C1 · unabhängige physische Prüfung der Operator-Dateien · 2026-10-11

```text
OBJECT = NEXUS_OMEGA_AXIOM_R27F_META_STACK_INDEPENDENT_INTAKE_AND_MINIMAL_INSTALL_PLAN_20261011_R0
PARENT = R27F_PR81_MAIN_54e83be730e225342fde477c266b63c1804537bd
PARENT_R27F_ORDER_SHA256 = 4f921fa413f437a13d9af5ef403beaa90e774015341f702017566b1880f04d3b
PARENT_R27E_ORDER_SHA256 = 86bae5b6e00d640a5c579ca1912410a2b8699b540add52aba741dd71c0e9a221
INPUT_PROVENANCE = OPERATOR_UPLOADED_META_LABELED_PACKAGE_NOT_PROVIDER_SIGNED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
EXECUTION = REPOSITORY_VALIDATOR_SOURCE_ONLY_NO_LIVE_RUNTIME
EXTERNAL_ACTOR_IDENTITY = UNVERIFIED
GITHUB_EXTERNAL_SEND = NO
ASSIGNMENT_R27F_REGISTERED = NO
PUBLIC_AGENT_RETURN_IMPORT = HOLD_STRUCTURE_AND_IDENTITY
ARCHIVE_FOLDER_X = READ_ONLY
CURSOR_NEW_WORKER = NO
WWW_HOSTINGER_DEPLOY = NO
```

## 1 · Source-exact local physical observations (not an authenticated provider attestation)

- Operator-uploaded `R27F_M~1.ZIP`: **22,870 bytes**, SHA256 `cab94a852e9462ac9dddb9511fcb0c2fa53519660bb57818f187c8da365050`. Separately uploaded ZIP receipt agrees.
- ZIP inventory: **12 non-directory members** in `returns/`: 7 prospective `R27F-00..06` files, 3 unrelated extra core objects (`00_EXTERNAL_AGENT_MANIFEST.json`, `01_README_RETURN_SLOT.md`, `TERMINAL_OBJECT_R27F_META_R0.md`), plus `SHA256SUMS.txt` and `R27F_MANIFEST_DETAILED_R0.json`. The accompanying receipt's `FILES_COUNT=10` means **ten core source objects**, not the full ZIP membership. These counters must not be conflated.
- All ten core file SHA-256 entries in `SHA256SUMS.txt` matched the actual ZIP member bytes. The **six** records in the R27-F return manifest each independently match member byte length, SHA-256 and Git blob SHA1 (`sha1("blob <bytes>\\0" + bytes)`). The manifest's own SHA256 is `a170e2358a69277c02507d6c1815f69c8418954f5bdff73c7a7ffc2e8e9c8844` from the ZIP bytes.
- Attached secondhand `R27F_A~1.MD` declares `AXIOM / GROK_4_7_VERIFICATION_INSTANCE`, and reports independent rehash. This is **not authenticated proof of AXIOM's or Grok provider's signature**, nor a GitHub API RECEIVE_ACK. AXIOM in this turn independently performs the local checks above.
- Neither entire ZIP nor the ten internal core objects are automatically imported into GitHub: their direct external GitHub send permission remains `DENY`, seven R27-F proposed filenames are **NOT_REGISTERED** in the NEXUS owned slot registry, and extraneous files contradict the exact seven-file contract.

## 2 · Independent scientific/structural adjudication of the content

**PASS_SOURCE_INTEGRITY_C1, HOLD_FULL_AGENT_RETURN_IMPORT**. Meaning: source bytes are coherent and furnish useful bounded research, but do not prove live ruleset modification, real external principal, production safety or completed model-performed experiments.

Major conclusions:

1. **Ruleset READBACK beats return prose.** The connected GitHub REST read on 2026-10-11 shows active `main-evidence-protection` ID `21252293` requiring only `validate` (integration 15368); `required_approving_review_count=0`; `require_code_owner_review=false`; but **`dismiss_stale_reviews_on_push=true`**, not `false` as claimed by the uploaded R27F-00 and R27F-01 texts. This is an actual factual disagreement; correct through successor commentary, not silent rewriting of submitted source.
2. **Do not invent GitHub identities.** `R27F-02` uses sample `grok-bot-app[bot]`, `meta-ai-research[bot]`, synthetic installation IDs `12345678/87654321` and `verified_at/verified_by/proof_ref` fields that could be mistaken for attested real principals. Classify `EXAMPLE_ONLY_UNVERIFIED_DO_NOT_INSTALL`. A real registration must be established through operator-authorized out-of-band verified GitHub App/account capability; no shared owner token.
3. **Return manifest fails machine contract.** The submitted `R27F-05` has uppercase `OBJECT`, `FILES`, `TOTAL_FILES`, etc., but the existing `schema/external-agent-return-r27e-v1.schema.json`/validator requires a **specific lowercase** set: `schema_version, agent_id, github_actor, parent_order_sha256, claim_ceiling, runtime, new_worker, axiom_ack, children`. The six source hashes are real, but it is not a valid seven-file GitHub return manifest. Its `parent_order_sha256` must match the NEXUS-owned assignment's current R27-F order only after a governed Registry change; no schema claim bypass.
4. **Fixture execution claims weakened.** `R27F-03` labels `EXECUTED_COUNT=3`, but E06 and I01 are primarily read-only statements taken from PR metadata, and a third PR-body parsing assertion is not accompanied by raw execution logs/seed/script/verified independent GitHub access. The document still usefully **DESIGNS fifteen tests**, but a reproducible `3/3` executed adversarial regression is `NOT_ESTABLISHED`. PR81 merging with a successful firewall check cannot demonstrate a bypass on a malicious PR.
5. **No standalone product to install.** This ZIP contains Markdown/JSON status, research recommendations, proposed identity examples and manifests, not a validated runnable broker, GitHub App installation package, Ruleset-admin change or Hostinger deployment. `INSTALL_EXTERNAL_AGENTS` and `START_LIVE_WAKE` remain forbidden/unavailable at these boundaries.
6. **Ruleset JSON in R27F-01 is only conceptual.** It is not a verified complete GitHub REST update payload and must not be sent verbatim to the GitHub Ruleset API; preserve all existing enforced rules and exact provider-supplied `integration_id` via GET/diff/PUT/readback only with a separately authorized administrator.

## 3 · Highest-value architectonic deduction (AXIOM own analysis, not claimed as Meta evidence)

**A structural firewall must be assignment-version agnostic while authority is assignment-specific.** The current `scripts/validate_external_agent_pr.py` has a hard-coded legacy manifest path `R27-05_RETURN_MANIFEST_R0.json`; this prevents correct future returns in the *same existing returns directory*. Repair **only that routing dependency** using the NEXUS-owned assignment `filenames` and explicit optional `manifest_filename`, with exact one-manifest validation. This change neither grants write permission nor creates a new directory. New unit tests must prove legacy backward compatibility, future assignment resolution, ambiguous manifest rejection, duplicate registered path rejection, and `R27F` still denied while unregistered.

This is a modularity improvement, not activation: the **authorization rule remains** `operator-registered real GitHub actor + ACTIVE_AUTHORIZED assignment + verified complete source/manifest + required GitHub ruleset + independent AXIOM readback`.

Further, a new provider-neutral **origin witness** is needed to distinguish bytes observed from actual model/provider identity. A SHA proves the return's bytes. It does not prove that the named AI generated it. Separate `CLAIMED_MODEL_ORIGIN`, `TRANSFERRED_BY_OPERATOR`, `SOURCE_EXACT_BYTE_VERIFIED`, `GITHUB_ACCOUNT_AUTHENTICATED`, `MODEL_PROVIDER_ATTESTED`. Leave the last two UNVERIFIED unless supplied by the real backend provider, not by an invented account object.

## 4 · Immediate safe release scope and remaining owner-only gates

**This GitHub PR installs only a minimal backwards-compatible validator hardening and accompanying existing test suite changes**, plus this one audit object under the **existing** `research/r27/www-extern-wake-isolation-20261011/` directory. No added top-level/return folder, no foreign account registration, no ZIP archive/ten-file dump, no new worker, no Hostinger deploy.

Premerge CI is mandatory, including `validate-repository-structure`, `r27e-external-structural-firewall` on a trusted base checkout, and `semgrep-cloud-platform/scan` for executable validator code. The NEXUS operator can separately enable the required firewall check and code owner review in the existing Ruleset after explicitly reviewing actual admin access; the present GitHub connector is not an admin authority. An authentic R27-F return slot remains unregistered until this distinct governance action.

**Decision:** `PASS_WITH_CAVEATS_C1_SOURCE_RESEARCH`; `PASS_CODE_HARDENING` only after test logs/CI; `R27F_RETURN_IMPORTED=NO`; `R27_AUTH001_002_003=HOLD_SECURITY`; `WWW_B2_B3=NOT_VERIFIED`; `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`.

*NEXUS OMEGA — Der äußere Befund darf Lernen auslösen; die konkrete interne Wirkung benötigt geprüfte Autorität. Mehr Bytes ohne zusätzliche Evidenz sind keine Verbesserung.*
