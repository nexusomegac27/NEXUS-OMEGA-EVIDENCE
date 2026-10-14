# LEGAL_RIGHTS_AND_PROVENANCE_BOUNDARIES.md (Lane L) — C1, factual source validation, no legal advice

## L1 — Pinned source identity (executed read-only)

- Repository morluto/rea at pinned commit 0f55f247cdd2ae9bd7903d5e45962b19dfc233dc: tree readable via authenticated GitHub read-back; root contains .agents, .github, .gitignore, .gitmodules, .gitattributes, package.json, LICENSE among others.
- package.json at that commit: name "rea-agents", version "6.5.0", license "MIT", repository git+https://github.com/morluto/rea.git. LICENSE at that commit: MIT License, Copyright (c) 2026 morluto.
- npm registry metadata (https://registry.npmjs.org/rea-agents, read-only, no install): dist-tags.latest = "6.5.0", license MIT, maintainer morluto, versions begin at 0.2.1.
- NOT asserted: that the shipped npm tarball equals the pinned Git tree. That would require actual tarball integrity and file-by-file correspondence, which was not performed here (no download, no install, per order).

## L2 — Lookalike repository (factual characterization only)

rea-githu/REA exists (default-branch commit 6f0454c6b4b15b2284d35e0cd9611293afe81243, read-only). Its README states: "REA Reverse Engineer Anything 6.3.0 (October 10, 2026) is the local MCP zip. rea github, github rea, reverse engineer anything, rea mcp, morluto rea." and advertises a downloadable x64 zip with "Source needed? No." The text embeds the morluto/rea brand name as a search keyword. Recorded as public evidence of misleading packaging (brand-riding, keyword stuffing, binary-zip distribution without source). NOT evidence of malware: the artifact was not obtained and not examined; nothing was downloaded to any operator system; no malicious-code claim is made. Examination would require separate authorization and a disposable analysis environment.

## L3 — CJEU C-13/20 Top System and German §§69d/69e (source-validated)

- The relevant judgment is C-13/20, Top System SA v Belgian State, 6 October 2021, ECLI:EU:C:2021:811 (Directive 91/250/EEC Art. 5(1)): the lawful purchaser of a computer program may decompile all or part of it insofar as necessary to correct errors affecting its operation, including by deactivating a function; decompilation for error correction does not require satisfying Art. 6, which has a different scope and purpose (interoperability). Direct EUR-Lex readback (https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A62020CJ0013) was blocked by a JavaScript/robot gate in this environment (UNAVAILABLE by direct fetch, honestly recorded); judgment content was validated through multiple independent secondary sources quoting operative paragraphs (ipcuria.eu case page C-13/20 paras 54-62; law-firm analyses berggren.eu, cuatrecasas.com, stibbe.com; acr.amsterdam case database).
- Germany: §69d UrhG ("Ausnahmen von den zustimmungsbedürftigen Handlungen") — absent special contractual terms, the acts of §69c Nr. 1-2 do not require the rightholder's consent insofar as they are necessary for the intended use of the program, including error correction ("insbesondere die Fehlerberichtigung"); §69e UrhG ("Dekompilierung") — reproduction/translation of the code does not require consent insofar as indispensable to obtain interoperability information, under strict conditions. The two provisions are distinct, exactly as the order requires. (§69d text read at https://dejure.org/gesetze/UrhG/69d.html mirror; §69e confirmed via gesetze-im-internet.de title/snippet and dejure.org mirror; gesetze-im-internet direct fetch was temporarily unreachable in this session.)
- The prior citation C-650/17 for error-correction decompilation was incorrect and remains corrected (R5 errata upheld). No blanket third-party reverse-engineering, disclosure or deployment authorization follows from any of these sources. A full legal opinion for third-party analysis is out of scope without licensed legal review.

## L4 — Live public index re-test (executed)

Live readback of PUBLIC_RESEARCH_INDEX.json (commit 165ab9638920b907c4a48869ee770fdd8e410168): the manifest lists SEVEN files, each with a 64-hex sha256 and byte count; all seven were re-fetched and independently rehashed in this return: 7/7 byte-exact, 7/7 SHA-256 match (see SOURCE_AND_CUSTODY_LEDGER.json). No self-entry; no SHA-1 in a SHA-256 field. Therefore: (a) the earlier expert allegation of a self-entry defect remains refuted — no repair task exists; (b) NEW FINDING: the R6 order text (§6 L4) and the foundation capsule (point 5) state the live index contains "six" entries; the live manifest contains seven (the evidence JSON was added after those documents were written). One-word correction required in both documents; no other defect.

## L5 — Redaction and publication boundaries applied to this return

No private ZIP payloads, credentials, operator signer material, proprietary decompilation or private path structures are included in this bundle. Only public C1 research pages and read-only public metadata are linked. This publication is a branch push to the authorized research branch, NOT a main merge and NOT a receiver ACK; the publisher hash is custody-neutral and never a CURSOR_ACK. Hostinger writes remain fail-closed.
