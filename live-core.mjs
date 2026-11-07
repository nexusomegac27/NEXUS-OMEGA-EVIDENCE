/* NEXUS OMEGA: Bodytwin public automatic updates, C1_DESCRIPTIVE_ONLY. */
export const RULE=Object.freeze({
 schema:'nexus-bodytwin-live-feed/1',
 ceiling:'C1_DESCRIPTIVE_ONLY',
 endpoint:'/bodytwin/live/current.json',
 refreshMilliseconds:60000,
 staleMilliseconds:1200000,
 maxResponseBytes:25000,
 requestTimeoutMilliseconds:9000
});
const exactly=(o,keys)=>o!==null&&typeof o==='object'&&!Array.isArray(o)&&
 Object.keys(o).length===keys.length&&keys.every(k=>Object.hasOwn(o,k));
const hex64=s=>typeof s==='string'&&/^[0-9a-f]{64}$/.test(s);
const utc=s=>typeof s==='string'&&/^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$/.test(s)&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().replace('.000Z','Z')===s;
const count=n=>Number.isSafeInteger(n)&&n>=0&&n<=100000;
export function validateFeed(f){
 if(!exactly(f,['schema','claim_ceiling','trust','producer','sources','bodytwin','research','gates']))throw Error('SCHEMA_KEYS');
 if(f.schema!==RULE.schema||f.claim_ceiling!==RULE.ceiling||f.trust!=='SELF_HOSTED_PUBLIC_C1_NOT_INDEPENDENT_WITNESS')throw Error('CLAIM_TRUST');
 if(!exactly(f.producer,['run_utc','seq','interval_seconds','source_changed','last_change_utc'])||
   !utc(f.producer.run_utc)||!utc(f.producer.last_change_utc)||
   !Number.isSafeInteger(f.producer.seq)||f.producer.seq<1||f.producer.interval_seconds!==300||
   typeof f.producer.source_changed!=='boolean')throw Error('INVALID_PRODUCER');
 if(Date.parse(f.producer.last_change_utc)>Date.parse(f.producer.run_utc))throw Error('INVERTED_EVENT_TIME');
 if(!exactly(f.sources,['bodytwin_state','research_receipt']))throw Error('SOURCES');
 for(const [key,path] of [['bodytwin_state','/research/bodytwin/state.json'],['research_receipt','/bodytwin/live/receipts.public.json']]){
  const source=f.sources[key];if(!exactly(source,['url','sha256'])||source.url!==path||!hex64(source.sha256))throw Error('SOURCE_INTEGRITY_'+key);
 }
 if(!exactly(f.bodytwin,['state','validated','consent','trial']))throw Error('BODYTWIN_KEYS');
 for(const [key,v] of [['state','RESEARCH_FOUNDATION_C1'],['validated','NO'],['consent','OPEN'],['trial','DESIGNED_NOT_EXECUTED']]){
  if(f.bodytwin[key]!==v)throw Error('BODYTWIN_HOLD_'+key);
 }
 if(!exactly(f.research,['source_date','source_object','status','node_pass','node_total','mutation_pass','mutation_total','schema_pass','schema_total']))throw Error('RESEARCH_KEYS');
 if(!/^20\d\d-\d\d-\d\d$/.test(f.research.source_date)||
   f.research.source_object!=='NEXUS_OMEGA_AXIOM_R14_R2R1_WINDOWS_PORTABILITY_HARNESS_REPAIR_HANDOFF_20261107_R0'||
   f.research.status!=='CURSOR_REPORTED_PASS_C1')throw Error('RESEARCH_PROVENANCE');
 for(const [a,b] of [['node_pass','node_total'],['mutation_pass','mutation_total'],['schema_pass','schema_total']]){
  if(!count(f.research[a])||!count(f.research[b])||f.research[a]>f.research[b])throw Error('RESEARCH_COUNTS');
 }
 if(!exactly(f.gates,['a72','r13_stage_ii','physical_imu','bodytwin_validated','consent','gate_v2']))throw Error('GATE_KEYS');
 for(const [k,v] of [['a72','SOURCE_GAP'],['r13_stage_ii','HOLD_DEPLOY_GAP'],['physical_imu','NOT_AUTHORIZED'],
   ['bodytwin_validated','NO'],['consent','OPEN'],['gate_v2','HOLD_R9_MJS_PREREQUISITE']]){
   if(f.gates[k]!==v)throw Error('UNAUTHORIZED_GATE_'+k);
 }
 return f;
}
export function classifyFreshness(feed,nowWallMilliseconds,hidden=false){
 if(!feed)return 'HOLD_NO_FEED';
 if(hidden)return 'HOLD_TAB_HIDDEN';
 if(!Number.isFinite(nowWallMilliseconds))return 'HOLD_DEVICE_CLOCK';
 const delta=nowWallMilliseconds-Date.parse(feed.producer.run_utc);
 if(delta< -300000)return 'HOLD_DEVICE_CLOCK_FUTURE';
 if(delta>RULE.staleMilliseconds)return 'HOLD_STALE_FEED';
 return 'PUBLIC_REFRESH_OBSERVED_C1';
}
export function checkSequence(previousSeq,nextSeq){
 if(previousSeq===null)return 'FIRST_WITNESS';
 if(!Number.isSafeInteger(previousSeq)||!Number.isSafeInteger(nextSeq))return 'HOLD_INVALID_SEQUENCE';
 if(nextSeq<previousSeq)return 'HOLD_SEQUENCE_ROLLBACK';
 if(nextSeq===previousSeq)return 'NO_NEW_PRODUCER_TICK';
 return 'NEW_PRODUCER_TICK';
}
