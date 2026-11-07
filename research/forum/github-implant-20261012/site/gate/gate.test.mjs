/* NEXUS OMEGA Gate V2 | disposable adversarial structural tests | no live requests */
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {
 CONTRACT,sourcePath,sourceUrl,liveUrl,validateReleaseManifest,
 parseGitHubContent,digest,compareFile,classify,isC1Marked,statusIsStale
} from './gate-core.mjs';
const GOOD='a'.repeat(40),BADSHA='b'.repeat(64),SHA='c'.repeat(64);
function manifest(){return {schema:'nexus-gate-release-v2',claim_ceiling:'C1_DESCRIPTIVE_ONLY',target_root:'/forum/github-implant/',release_ref:GOOD,
 files:Object.fromEntries(CONTRACT.files.map(f=>[f,{bytes:125,sha256:SHA}]))};}
const pairs=()=>CONTRACT.files.map(file=>({file,status:'MATCH',gh:{sha:SHA,bytes:125},www:{sha:SHA,bytes:125}}));
function changed(mut){const m=manifest();mut(m);return m;}
for(const [name,fn] of [
 ['manifest valid',(m)=>{}],
 ['manifest missing version',m=>delete m.schema],
 ['manifest extra field',m=>m.unknown=true],
 ['manifest wrong version',m=>m.schema='v3'],
 ['manifest missing C1',m=>m.claim_ceiling='C2_PROVEN'],
 ['manifest blank SHA',m=>m.release_ref=''],
 ['manifest SHA uppercase',m=>m.release_ref=GOOD.toUpperCase()],
 ['manifest SHA length 39',m=>m.release_ref='a'.repeat(39)],
 ['manifest wrong target',m=>m.target_root='/other/'],
 ['manifest array filelist',m=>m.files=[]],
 ['manifest missing file',m=>delete m.files['index.html']],
 ['manifest unknown file',m=>m.files['secrets/.env']={bytes:2,sha256:SHA}],
 ['manifest short sha',m=>m.files['index.html'].sha256='abc'],
 ['manifest uppercase sha',m=>m.files['index.html'].sha256=SHA.toUpperCase()],
 ['manifest fractional bytes',m=>m.files['index.html'].bytes=1.5],
 ['manifest zero bytes',m=>m.files['index.html'].bytes=0],
 ['manifest oversized file',m=>m.files['index.html'].bytes=700000],
 ['manifest extra file property',m=>m.files['index.html'].extra='x'],
 ['manifest null file object',m=>m.files['index.html']=null]
]) {
 test(name,()=>{const m=manifest();fn(m);if(name==='manifest valid') assert.equal(validateReleaseManifest(m).sourceCommit,GOOD);
 else assert.throws(()=>validateReleaseManifest(m));});
}
test('file scope=10 fixed',()=>{assert.equal(CONTRACT.files.length,10);assert.equal(new Set(CONTRACT.files).size,10);});
test('GitHub pin is immutable and encoded',()=>assert.match(sourceUrl('index.html',GOOD),/ref=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa$/));
test('GitHub refuses moving main ref',()=>assert.throws(()=>sourceUrl('index.html','main')));
test('GitHub refuses path traversal',()=>assert.throws(()=>sourcePath('../../.env')));
test('Live origin uses exact fixed path',()=>assert.equal(liveUrl('gate/gate.js','https://www.nexus-mobile.de'),'https://www.nexus-mobile.de/forum/github-implant/gate/gate.js'));
test('Live origin refuses http',()=>assert.throws(()=>liveUrl('index.html','http://www.nexus-mobile.de')));
test('Live origin refuses unlisted path',()=>assert.throws(()=>liveUrl('.env','https://www.nexus-mobile.de')));
test('valid GitHub base64',()=>{
 const raw='NEXUS\n';const meta={encoding:'base64',content:Buffer.from(raw).toString('base64'),sha:GOOD,size:raw.length};
 assert.equal(new TextDecoder().decode(parseGitHubContent(meta)),raw);
});
test('GitHub content bad SHA1',()=>assert.throws(()=>parseGitHubContent({encoding:'base64',content:'YWJj',sha:'abc',size:3})));
test('GitHub content wrong length',()=>assert.throws(()=>parseGitHubContent({encoding:'base64',content:'YWJj',sha:GOOD,size:4})));
test('GitHub content invalid base64',()=>assert.throws(()=>parseGitHubContent({encoding:'base64',content:'YW=j',sha:GOOD,size:3})));
test('GitHub content oversize',()=>assert.throws(()=>parseGitHubContent({encoding:'base64',content:'YWJj',sha:GOOD,size:700000})));
test('SHA-256 known answer',async()=>assert.equal(await digest(new TextEncoder().encode('abc')),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'));
test('correct three-way comparison',()=>assert.equal(compareFile('index.html',{sha256:SHA,bytes:125},{sha:SHA,bytes:125},{sha:SHA,bytes:125}).status,'MATCH'));
test('GitHub missing',()=>assert.equal(compareFile('index.html',{sha256:SHA,bytes:125},null,{sha:SHA,bytes:125}).status,'SOURCE_GAP'));
test('WWW missing',()=>assert.equal(compareFile('index.html',{sha256:SHA,bytes:125},{sha:SHA,bytes:125},null).status,'WWW_GAP'));
test('GitHub mismatches pinned release',()=>assert.equal(compareFile('index.html',{sha256:SHA,bytes:125},{sha:BADSHA,bytes:125},{sha:SHA,bytes:125}).status,'RELEASE_SOURCE_MISMATCH'));
test('WWW mismatches pinned release',()=>assert.equal(compareFile('index.html',{sha256:SHA,bytes:125},{sha:SHA,bytes:125},{sha:BADSHA,bytes:125}).status,'WWW_RELEASE_MISMATCH'));
test('WWW length differs even if hash same',()=>assert.equal(compareFile('index.html',{sha256:SHA,bytes:125},{sha:SHA,bytes:125},{sha:SHA,bytes:124}).status,'WWW_RELEASE_MISMATCH'));
test('positive complete C1 verdict',()=>assert.equal(classify(pairs(),true,true,GOOD).code,'MATCH_C1'));
test('GitHub main drift does not affect release result',()=>assert.equal(classify(pairs(),true,true,'d'.repeat(40)).code,'MATCH_C1'));
test('missing release bind fails closed',()=>assert.equal(classify(pairs(),false,true,GOOD).code,'HOLD_RELEASE_BIND'));
test('missing one row fails closed',()=>assert.equal(classify(pairs().slice(1),true,true,GOOD).code,'HOLD_SCOPE'));
test('duplicate row fails closed',()=>{const r=pairs();r[1]=r[0];assert.equal(classify(r,true,true,GOOD).code,'HOLD_SCOPE');});
test('GitHub not reachable holds',()=>{const r=pairs();r[0].status='SOURCE_GAP';assert.equal(classify(r,true,true,GOOD).code,'HOLD_SOURCE');});
test('WWW 404 holds',()=>{const r=pairs();r[0].status='WWW_GAP';assert.equal(classify(r,true,true,GOOD).code,'HOLD_WWW');});
test('byte divergence refuses C1',()=>{const r=pairs();r[0].status='WWW_RELEASE_MISMATCH';assert.equal(classify(r,true,true,GOOD).code,'DIVERGENCE');});
test('C1 missing refuses PASS',()=>assert.equal(classify(pairs(),true,false,GOOD).code,'SCIENCE_WARN'));
test('C1 marked source',()=>assert.equal(isC1Marked('CLAIM_CEILING = C1_DESCRIPTIVE_ONLY'),true));
test('C2 promotion rejects C1 text marker',()=>assert.equal(isC1Marked('C1_DESCRIPTIVE_ONLY C2_PROVEN'),false));
test('stale at precise 30min boundary',()=>assert.equal(statusIsStale(500,500+1800000,false),true));
test('fresh just before boundary',()=>assert.equal(statusIsStale(500,500+1799999,false),false));
test('background tab invalidates observation',()=>assert.equal(statusIsStale(500,501,true),true));
test('clock epoch rollback invalidates observation',()=>assert.equal(statusIsStale(500,499,false),true));
test('missing clock reading is stale',()=>assert.equal(statusIsStale(NaN,Infinity,false),true));
