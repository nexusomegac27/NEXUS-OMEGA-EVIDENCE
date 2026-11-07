import test from 'node:test';
import assert from 'node:assert/strict';
import {RULE,validateFeed,classifyFreshness,checkSequence} from '../site/live-core.mjs';
const hex='a'.repeat(64);
const sample=()=>({
 schema:RULE.schema,claim_ceiling:RULE.ceiling,trust:'SELF_HOSTED_PUBLIC_C1_NOT_INDEPENDENT_WITNESS',
 producer:{run_utc:'2026-11-07T19:00:00Z',seq:1,interval_seconds:300,source_changed:true,last_change_utc:'2026-11-07T19:00:00Z'},
 sources:{bodytwin_state:{url:'/research/bodytwin/state.json',sha256:hex},research_receipt:{url:'/bodytwin/live/receipts.public.json',sha256:hex}},
 bodytwin:{state:'RESEARCH_FOUNDATION_C1',validated:'NO',consent:'OPEN',trial:'DESIGNED_NOT_EXECUTED'},
 research:{source_date:'2026-11-07',source_object:'NEXUS_OMEGA_AXIOM_R14_R2R1_WINDOWS_PORTABILITY_HARNESS_REPAIR_HANDOFF_20261107_R0',status:'CURSOR_REPORTED_PASS_C1',node_pass:177,node_total:177,mutation_pass:7,mutation_total:7,schema_pass:18,schema_total:18},
 gates:{a72:'SOURCE_GAP',r13_stage_ii:'HOLD_DEPLOY_GAP',physical_imu:'NOT_AUTHORIZED',bodytwin_validated:'NO',consent:'OPEN',gate_v2:'HOLD_R9_MJS_PREREQUISITE'}
});
test('C1 valid feed',()=>assert.equal(validateFeed(sample()).producer.seq,1));
const rejects=[
 ['extra user health field',x=>x.health='private'],
 ['nested extra field',x=>x.research.person='private'],
 ['C2 promotion',x=>x.claim_ceiling='C2_VALIDATED'],
 ['reliability claim',x=>x.trust='EXTERNAL_TRUSTED_WITNESS'],
 ['fake sensor',x=>x.gates.physical_imu='ACTIVE'],
 ['fake body validation',x=>x.bodytwin.validated='YES'],
 ['fake consent',x=>x.bodytwin.consent='GRANTED'],
 ['fake trial',x=>x.bodytwin.trial='RUNNING'],
 ['A72 closure',x=>x.gates.a72='CLOSED'],
 ['R13 stage promotion',x=>x.gates.r13_stage_ii='DONE'],
 ['Gate V2 promotion',x=>x.gates.gate_v2='PASS'],
 ['wrong source URL',x=>x.sources.bodytwin_state.url='https://bad.example'],
 ['invalid source sha',x=>x.sources.research_receipt.sha256='nohash'],
 ['missing source',x=>delete x.sources.research_receipt],
 ['bad claim type',x=>x.claim_ceiling=false],
 ['bad producer seq',x=>x.producer.seq=0],
 ['bad producer fractional seq',x=>x.producer.seq=1.1],
 ['bad producer interval',x=>x.producer.interval_seconds=10],
 ['bad UTC timestamp',x=>x.producer.run_utc='yesterday'],
 ['invalid calendar date',x=>x.producer.run_utc='2026-02-30T19:00:00Z'],
 ['inverted change timestamps',x=>x.producer.last_change_utc='2026-11-07T20:00:00Z'],
 ['invalid source object',x=>x.research.source_object='INVENTED'],
 ['invalid source status',x=>x.research.status='SCIENCE_VALIDATED'],
 ['node pass exceeds total',x=>x.research.node_pass=200],
 ['negative mutation count',x=>x.research.mutation_pass=-1],
 ['extra producer field',x=>x.producer.witness='TRUSTED'],
 ['source changed must be boolean',x=>x.producer.source_changed='false'],
];
for(const [name,mutation] of rejects)test('FAIL_CLOSED '+name,()=>{const x=sample();mutation(x);assert.throws(()=>validateFeed(x));});
test('fresh at observation',()=>assert.equal(classifyFreshness(sample(),Date.parse('2026-11-07T19:01:00Z')),'PUBLIC_REFRESH_OBSERVED_C1'));
test('stale at +20min boundary',()=>assert.equal(classifyFreshness(sample(),Date.parse('2026-11-07T19:21:00Z')),'HOLD_STALE_FEED'));
test('future feed +6min',()=>assert.equal(classifyFreshness(sample(),Date.parse('2026-11-07T18:54:00Z')),'HOLD_DEVICE_CLOCK_FUTURE'));
test('hidden tab',()=>assert.equal(classifyFreshness(sample(),Date.parse('2026-11-07T19:01:00Z'),true),'HOLD_TAB_HIDDEN'));
test('untrusted clock',()=>assert.equal(classifyFreshness(sample(),NaN),'HOLD_DEVICE_CLOCK'));
test('no feed',()=>assert.equal(classifyFreshness(null,Date.now()),'HOLD_NO_FEED'));
test('first sequence',()=>assert.equal(checkSequence(null,1),'FIRST_WITNESS'));
test('same sequence',()=>assert.equal(checkSequence(1,1),'NO_NEW_PRODUCER_TICK'));
test('incremented sequence',()=>assert.equal(checkSequence(1,2),'NEW_PRODUCER_TICK'));
test('rollback sequence',()=>assert.equal(checkSequence(12,11),'HOLD_SEQUENCE_ROLLBACK'));
test('malformed sequence',()=>assert.equal(checkSequence(NaN,12),'HOLD_INVALID_SEQUENCE'));
