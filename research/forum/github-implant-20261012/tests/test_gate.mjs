/* Node.js 22 built-in test runner · SPDX-License-Identifier: Apache-2.0 */
import test from "node:test";
import assert from "node:assert/strict";
import { CONTRACT, classify, digest, isC1Marked, parseGitHubContent, safeGitHubUrl } from "../site/gate/gate-core.mjs";
test("three exact scoped interface files only",()=>assert.deepEqual(CONTRACT.files,["index.html","assets/github-implant.css","assets/github-implant.js"]));
test("valid content: size and base64",()=>assert.equal(new TextDecoder().decode(parseGitHubContent({encoding:"base64",content:"YWJj",size:3,sha:"a".repeat(40)})),"abc"));
test("bad source size fails",()=>assert.throws(()=>parseGitHubContent({encoding:"base64",content:"YWJj",size:4,sha:"a".repeat(40)})));
test("non base64 fails",()=>assert.throws(()=>parseGitHubContent({encoding:"utf-8",content:"abc",size:3,sha:"a".repeat(40)})));
test("scoped matching bytes are C1 not truth",()=>assert.equal(classify([{status:"MATCH"},{status:"MATCH"},{status:"MATCH"}],true,true).code,"MATCH_C1"));
test("source API unavailable -> source HOLD",()=>assert.equal(classify([],false,true).code,"HOLD_SOURCE"));
test("one missing site asset -> WWW HOLD",()=>assert.equal(classify([{status:"MATCH"},{status:"ERROR"},{status:"MATCH"}],true,true).code,"HOLD_WWW"));
test("byte divergence detected",()=>assert.equal(classify([{status:"MATCH"},{status:"DIVERGENT"},{status:"MATCH"}],true,true).code,"DIVERGENCE"));
test("missing C1 label warning",()=>assert.equal(classify([{status:"MATCH"},{status:"MATCH"},{status:"MATCH"}],true,false).code,"SCIENCE_WARN"));
test("partial observation blocked",()=>assert.equal(classify([{status:"MATCH"}],true,true).code,"HOLD_SCOPE"));
test("C1 marker recognition",()=>{assert.equal(isC1Marked("CLAIM_CEILING=C1_DESCRIPTIVE_ONLY"),true);assert.equal(isC1Marked("SCIENCE"),false)});
test("URL safety",()=>{assert.equal(safeGitHubUrl("https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/main/README.md"),true);assert.equal(safeGitHubUrl("https://github.com.attacker.invalid/path"),false)});
test("webcrypto SHA-256 known answer",async()=>{assert.equal(await digest(new TextEncoder().encode("abc")),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")});
