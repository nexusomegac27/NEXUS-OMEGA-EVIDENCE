'use strict';
// Isolated C1 source-bound wrapper; the V1 classifier remains immutable.
const crypto=require('crypto');
const {classify}=require('./alpha_ci_pr_path_filter_audit_v1_20261031.js');
const PIN=Object.freeze({bytes:8685,sha256:'9aad5e271db570dc13b5ad2e7d8a3fbd9bc3db4de2e4b13b96390614dbf2c0fd'});
function classifyPinnedText(raw){
 const fail=reason=>({status:'FAIL_CLOSED',reason});
 if(typeof raw!=='string'||Buffer.byteLength(raw,'utf8')!==PIN.bytes)return fail('source_bytes');
 if(crypto.createHash('sha256').update(raw,'utf8').digest('hex')!==PIN.sha256)return fail('source_sha256');
 let parsed;try{parsed=JSON.parse(raw);}catch(_){return fail('invalid_json');}
 return classify(parsed);
}
if(require.main===module){
 let result;try{result=classifyPinnedText(require('fs').readFileSync(0,'utf8'));}
 catch(_){result={status:'FAIL_CLOSED',reason:'io_or_runtime'};}
 process.stdout.write(JSON.stringify(result)+String.fromCharCode(10));
 if(result.status!=='PASS')process.exitCode=2;
}
module.exports={classifyPinnedText,PIN};
