/* NEXUS OMEGA C1 frozen independent structural evaluator; no provider authentication, no production integration. */
"use strict";
const EXPECTED=[
  {
    "pr": 295,
    "parent": "b650d9361b58bc6cc9235f97a68edf732336f4eb",
    "main": "0c6e9385ad4fb7fdd9a0ee384427460e568b2809",
    "receipt": 6582097904,
    "file_count": 2
  },
  {
    "pr": 296,
    "parent": "0c6e9385ad4fb7fdd9a0ee384427460e568b2809",
    "main": "0c6595660cc51cafe0d0d5a7daeeb7007defe9b1",
    "receipt": 6583755114,
    "file_count": 3
  },
  {
    "pr": 297,
    "parent": "0c6595660cc51cafe0d0d5a7daeeb7007defe9b1",
    "main": "a55f1026a6cf418f89b6c7c916bd015d55dffd13",
    "receipt": 6585520284,
    "file_count": 3
  },
  {
    "pr": 298,
    "parent": "a55f1026a6cf418f89b6c7c916bd015d55dffd13",
    "main": "013ee6b3027eb8f8b172ea72aec5b6812316d386",
    "receipt": 6586901931,
    "file_count": 3
  },
  {
    "pr": 299,
    "parent": "013ee6b3027eb8f8b172ea72aec5b6812316d386",
    "main": "a3e8b63ecb52f27cef1177ad2bab86057804bbbb",
    "receipt": 6588025294,
    "file_count": 3
  },
  {
    "pr": 300,
    "parent": "a3e8b63ecb52f27cef1177ad2bab86057804bbbb",
    "main": "94ea6517cc7a9f98a53cc8c4fb5f6a3d6fd9c6f8",
    "receipt": 6588842440,
    "file_count": 3
  },
  {
    "pr": 307,
    "parent": "94ea6517cc7a9f98a53cc8c4fb5f6a3d6fd9c6f8",
    "main": "88e7bb6aa41f15bb1127753e869e0cd38b74f031",
    "receipt": 6590159318,
    "file_count": 3
  },
  {
    "pr": 308,
    "parent": "88e7bb6aa41f15bb1127753e869e0cd38b74f031",
    "main": "bbdb0eaf5382f4dd880f20c1a417ad4c80990b25",
    "receipt": 6591500315,
    "file_count": 3
  }
];
function assess(rows){
 if(!Array.isArray(rows)||rows.length!==EXPECTED.length)return {status:"NOT_COMPUTABLE",reason:"COHORT_POPULATION"};
 const seen=new Set();let total=0;
 for(let i=0;i<EXPECTED.length;i++){
  const e=EXPECTED[i],r=rows[i];
  if(!r||r.pr!==e.pr)return {status:"NOT_COMPUTABLE",reason:"PR_ID"};
  if(r.parent!==e.parent||r.main!==e.main||r.receipt_main!==e.main||i>0&&r.parent!==rows[i-1].main)return {status:"NOT_COMPUTABLE",reason:"MAIN_CHAIN"};
  if(r.receipt!==e.receipt||seen.has(r.receipt))return {status:"NOT_COMPUTABLE",reason:"RECEIPT_BINDING"};
  if(r.file_count!==e.file_count||r.added_files!==e.file_count||r.verified_files!==e.file_count)return {status:"NOT_COMPUTABLE",reason:"FILE_COVERAGE"};
  if(r.file_sha256_match!==true||r.file_blob_match!==true||r.file_bytes_match!==true)return {status:"NOT_COMPUTABLE",reason:"BYTE_BINDING"};
  if(!Number.isSafeInteger(r.verified_bytes)||r.verified_bytes<=0)return {status:"NOT_COMPUTABLE",reason:"BYTE_COUNT"};
  total+=r.verified_bytes;seen.add(r.receipt);
 }
 if(total!==106901)return {status:"NOT_COMPUTABLE",reason:"TOTAL_BYTES"};
 return {status:"BOUNDED_SOURCE_RECONCILED",numerator:8,denominator:8,files:23,bytes:total,limitation:"DECLARED_RECORDS_NOT_PROVIDER_AUTHENTICATION"};
}
function runTests(){
 const base=EXPECTED.map(e=>({...e,receipt_main:e.main,added_files:e.file_count,verified_files:e.file_count,file_sha256_match:true,file_blob_match:true,file_bytes_match:true,verified_bytes:[11004,13281,15065,12978,13475,11814,15008,14276][EXPECTED.findIndex(x=>x.pr===e.pr)]}));
 // Per-PR byte totals are adjusted to the 106901-byte physical source census.
 const physical=[11004,13281,15065,12978,13475,11814,15008,14276];
 const delta=106901-physical.reduce((s,x)=>s+x,0);base[7].verified_bytes+=delta;
 const mutate=(i,p)=>base.map((r,j)=>j===i?{...r,...p}:{...r});
 const cases=[
 ["positive",base,"BOUNDED_SOURCE_RECONCILED"],
 ["missing_pr",base.slice(1),"NOT_COMPUTABLE"],
 ["duplicate_pr",mutate(2,{pr:296}),"NOT_COMPUTABLE"],
 ["wrong_parent",mutate(4,{parent:base[2].main}),"NOT_COMPUTABLE"],
 ["wrong_main",mutate(3,{main:"f".repeat(40),receipt_main:"f".repeat(40)}),"NOT_COMPUTABLE"],
 ["wrong_receipt_main",mutate(5,{receipt_main:base[4].main}),"NOT_COMPUTABLE"],
 ["duplicate_receipt",mutate(6,{receipt:base[5].receipt}),"NOT_COMPUTABLE"],
 ["wrong_receipt",mutate(7,{receipt:999}),"NOT_COMPUTABLE"],
 ["missing_file",mutate(1,{verified_files:2}),"NOT_COMPUTABLE"],
 ["extra_file",mutate(0,{file_count:3}),"NOT_COMPUTABLE"],
 ["wrong_addition",mutate(2,{added_files:2}),"NOT_COMPUTABLE"],
 ["sha_mismatch",mutate(3,{file_sha256_match:false}),"NOT_COMPUTABLE"],
 ["blob_mismatch",mutate(4,{file_blob_match:false}),"NOT_COMPUTABLE"],
 ["bytes_mismatch",mutate(5,{file_bytes_match:false}),"NOT_COMPUTABLE"],
 ["zero_bytes",mutate(6,{verified_bytes:0}),"NOT_COMPUTABLE"],
 ["total_bytes_drift",mutate(7,{verified_bytes:base[7].verified_bytes+1}),"NOT_COMPUTABLE"]
 ];
 const results=cases.map(([name,rows,want])=>({name,pass:assess(rows).status===want}));
 return {passed:results.filter(x=>x.pass).length,total:results.length,results};
}
if(typeof module!=="undefined")module.exports={EXPECTED,assess,runTests};
