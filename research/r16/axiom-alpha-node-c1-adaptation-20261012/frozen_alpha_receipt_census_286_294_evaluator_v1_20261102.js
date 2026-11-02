/* NEXUS OMEGA Alpha C1 | frozen bounded receipt-census structural evaluator.
 * Research-only: caller-supplied records are NOT authenticated GitHub data.
 * Freeze this before the report candidate; no production integration.
 */
"use strict";
const BASE="ccfd6c4168f989bc372fe87227fd9218a77da6ff";
const TIP="b650d9361b58bc6cc9235f97a68edf732336f4eb";
const MERGES=[
"558dd66d4dd733236b628d0cd0894d96554db176",
"2fbce469dc8c66d33a4be14eacb97bac3b02b938",
"7ff9e7293c9f825716333ddbfd1a5227b2e6aa3f",
"bae9dc84fe030cf3214c55edd1d646640efc3811",
"c22382b1d7326ece4de940d06834ee5e5ba4964b",
"9b22820cc1943fe7753acf0ef4a25c68dee28930",
"9a99a14d6f50fdc95ae4d8199e29ef1bd8de3001",
"331cd4619040035ad940795ae93c1559f06e2913",
"b650d9361b58bc6cc9235f97a68edf732336f4eb"];
const RECEIPTS=[6570267138,6570434057,6573619590,6575253285,6576414292,6577253195,6579058793,6580456089,6581636281];
function assess(rows) {
  if(!Array.isArray(rows)||rows.length!==9) return {status:"NOT_COMPUTABLE",reason:"POPULATION_INCOMPLETE"};
  let previous=BASE;const seen=new Set();
  for(let i=0;i<9;i++){
    const r=rows[i];
    if(!r||r.pr!==286+i) return {status:"NOT_COMPUTABLE",reason:"PR_SEQUENCE"};
    if(r.parent!==previous||r.main!==r.receipt_main||r.main!==MERGES[i])
      return {status:"NOT_COMPUTABLE",reason:"COMMIT_BINDING"};
    if(!Number.isSafeInteger(r.receipt_id)||seen.has(r.receipt_id)||r.receipt_id!==RECEIPTS[i])
      return {status:"NOT_COMPUTABLE",reason:"RECEIPT_ID_BINDING"};
    if(r.changed_files!==3||r.added_files!==3||r.verified_files!==3)
      return {status:"NOT_COMPUTABLE",reason:"FILE_COVERAGE"};
    seen.add(r.receipt_id);previous=r.main;
  }
  if(previous!==TIP) return {status:"NOT_COMPUTABLE",reason:"TIP_MISMATCH"};
  return {status:"BOUNDED_COHORT_STRUCTURALLY_RECONCILED",numerator:9,denominator:9,
          evidence_class:"SUPPLIED_SNAPSHOT_ONLY_NOT_PROVIDER_AUTHENTICATED"};
}
function baselineRows(){
  return MERGES.map((main,i)=>({pr:286+i,parent:i?MERGES[i-1]:BASE,
    main,receipt_main:main,receipt_id:RECEIPTS[i],
    changed_files:3,added_files:3,verified_files:3}));
}
function mutated(rows,i,patch){return rows.map((r,j)=>j===i?{...r,...patch}:{...r});}
function runTests(){
  const b=baselineRows();
  const cases=[
    ["positive",b,"BOUNDED_COHORT_STRUCTURALLY_RECONCILED"],
    ["missing_event",b.slice(0,8),"NOT_COMPUTABLE"],
    ["wrong_receipt_main",mutated(b,3,{receipt_main:MERGES[2]}),"NOT_COMPUTABLE"],
    ["duplicate_receipt",mutated(b,5,{receipt_id:RECEIPTS[4]}),"NOT_COMPUTABLE"],
    ["missing_file",mutated(b,7,{verified_files:2}),"NOT_COMPUTABLE"],
    ["wrong_parent",mutated(b,6,{parent:MERGES[3]}),"NOT_COMPUTABLE"],
    ["wrong_pr",mutated(b,8,{pr:295}),"NOT_COMPUTABLE"],
    ["forged_middle",mutated(b,2,{main:"a".repeat(40),receipt_main:"a".repeat(40)}),"NOT_COMPUTABLE"]
  ];
  const out=cases.map(([name,data,expected])=>({name,pass:assess(data).status===expected}));
  // Falsifier: all fields can be jointly forged if the trusted constants
  // themselves are replaced. This is a LIMIT, not a success fixture.
  return {pass:out.filter(x=>x.pass).length,total:out.length,cases:out,
    provider_authentication:"NOT_PERFORMED",science_execution:"NOT_PROVEN"};
}
if(typeof module!=="undefined"&&module.exports)module.exports={assess,runTests};
