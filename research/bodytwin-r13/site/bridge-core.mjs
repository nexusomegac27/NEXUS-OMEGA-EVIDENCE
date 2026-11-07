/* NEXUS OMEGA R13 research-status bridge. PUBLIC C1 ONLY; no sensor API. */
export const RULE=Object.freeze({schema:'nexus-research-bodytwin-state/1',claimCeiling:'C1_DESCRIPTIVE_ONLY',source:'/research/bodytwin/state.json',maxBytes:12000,maxAgeMs:600000});
export const RESEARCH=Object.freeze({chain:'FIVE_MARKDOWN_SOURCE_HASHES_MATCH',qwenPdf:'ORIGINAL_13_PAGE_PDF_BYTE_BOUND_BY_AXIOM',a72:'SOURCE_GAP_ORIGINALS_MISSING',measurement:'NOT_EXECUTED',calibration:'DESIGN_ONLY',claim:'C1_DESCRIPTIVE_ONLY'});
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
const sameSet=(a,b)=>Array.isArray(a)&&a.length===b.length&&new Set(a).size===b.length&&b.every(x=>a.includes(x));
export function validatePublicState(s){
 if(!object(s))throw Error('NOT_OBJECT');
 const keys=['schema','object','BODYTWIN','BODYTWIN_VALIDATED','CONSENT_BIND','TRIAL_001','layers','pipeline','invariants','claim_ceiling','claim_promotion'];
 if(!sameSet(Object.keys(s),keys))throw Error('UNRECOGNIZED_SCHEMA_FIELDS');
 if(s.schema!==RULE.schema||s.object!=='BODYTWIN_PUBLIC_SURFACE')throw Error('BAD_SCHEMA');
 if(s.BODYTWIN!=='RESEARCH_FOUNDATION_C1'||s.BODYTWIN_VALIDATED!=='NO')throw Error('UNPROVEN_VALIDATION');
 if(s.CONSENT_BIND!=='OPEN'||s.TRIAL_001!=='DESIGNED_NOT_EXECUTED')throw Error('UNPROVEN_CONSENT_OR_TRIAL');
 if(s.claim_ceiling!==RULE.claimCeiling||s.claim_promotion!==false)throw Error('CLAIM_CEILING_VIOLATION');
 if(!sameSet(s.layers,['L0','L1','L2','L3','UNKNOWN_UNOBSERVED']))throw Error('LAYERS_MISMATCH');
 if(!sameSet(s.pipeline,['Capture','Normalize','Align','Refine','Metrics']))throw Error('PIPELINE_MISMATCH');
 if(!sameSet(s.invariants,['RAW_NE_REFINED','PHOTOREALISM_GAIN_MAY_CAUSE_IDENTITY_LOSS','NO_PRIVATE_HUMAN_REFERENCE_MEDIA']))throw Error('INVARIANTS_MISMATCH');
 return Object.freeze({state:s.BODYTWIN,validated:false,consent:s.CONSENT_BIND,trial:s.TRIAL_001,source:'PUBLIC_STATE_UNATTESTED',promotion:false});
}
export function freshness(previous,now,hidden){return !previous?'SOURCE_GAP':hidden||!Number.isFinite(now)||now<0||now>=RULE.maxAgeMs?'STALE_UNVERIFIED':'PUBLIC_STATUS_OBSERVED_C1';}
