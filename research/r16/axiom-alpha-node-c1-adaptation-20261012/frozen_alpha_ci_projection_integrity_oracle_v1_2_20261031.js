'use strict';
// Frozen before V2 candidate. Independent Node subprocess evaluator of the REAL pinned projection.
const fs=require('fs'), crypto=require('crypto'), assert=require('assert');
const {spawnSync}=require('child_process');
const [v1,v2,projection]=process.argv.slice(2);
if(!v1||!v2||!projection) throw Error('usage: node <oracle.js> <v1.js> <v2.js> <projection.json>');
const original=fs.readFileSync(projection);
const pin={bytes:8685,sha256:'9aad5e271db570dc13b5ad2e7d8a3fbd9bc3db4de2e4b13b96390614dbf2c0fd',blob:'5da248602def62f7d34c926ccc21bf59ec944bcb'};
assert.strictEqual(original.length,pin.bytes,'source byte length');
assert.strictEqual(crypto.createHash('sha256').update(original).digest('hex'),pin.sha256,'source SHA256');
assert.strictEqual(crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+original.length),Buffer.from([0]),original])).digest('hex'),pin.blob,'source Git blob');
const raw=original.toString('utf8');
function run(file,text,expectedStatus,expectedExit){
 const p=spawnSync(process.execPath,[file],{input:text,encoding:'utf8',timeout:5000,maxBuffer:1048576});
 if(p.error)throw p.error;
 assert.strictEqual(p.status,expectedExit,file+' exit status');
 let data;try{data=JSON.parse(p.stdout);}catch{throw Error(file+' non-JSON stdout');}
 assert.strictEqual(data.status,expectedStatus,file+' result');
 return data;
}
let tests=0;
const base1=run(v1,raw,'PASS',0),base2=run(v2,raw,'PASS',0);
for(const x of [base1,base2]){
 assert.strictEqual(x.workflows,17);assert.strictEqual(x.validate_definitions,12);
 assert.strictEqual(x.eligible,4);assert.strictEqual(x.filtered,8);
}tests+=2;
const tamperBlob=raw.replace('b03b029f7c168ac80ae42f3a40a3ad9481c367a7','a03b029f7c168ac80ae42f3a40a3ad9481c367a7');
const tamperFilter=raw.replace('research/ix/**','research/r8/**');
assert.notStrictEqual(tamperBlob,raw);assert.notStrictEqual(tamperFilter,raw);
assert.strictEqual(Buffer.byteLength(tamperBlob),pin.bytes);
assert.strictEqual(Buffer.byteLength(tamperFilter),pin.bytes);
for(const altered of [tamperBlob,tamperFilter]){
 run(v1,altered,'PASS',0);run(v2,altered,'FAIL_CLOSED',2);tests+=2;
}
// Removing only the terminal LF leaves valid JSON: V1 accepts it, V2 rejects changed bytes.
run(v1,raw.slice(0,-1),'PASS',0);run(v2,raw.slice(0,-1),'FAIL_CLOSED',2);tests+=2;
// An actually malformed JSON document must fail closed in both versions.
run(v1,'{"x":','FAIL_CLOSED',2);run(v2,'{"x":','FAIL_CLOSED',2);tests+=2;
process.stdout.write(JSON.stringify({oracle:'FROZEN_REAL_PROJECTION_BLACK_BOX_V1_2',tests,baseline_pass:2,tampered_same_length_rejected_by_v2:2,malformed_rejected:2,byte_variant_rejected_by_v2:1})+String.fromCharCode(10));
