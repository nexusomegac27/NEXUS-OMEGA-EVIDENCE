'use strict';
// Frozen independent black-box oracle: separate Node process, no import of candidate internals.
const {spawnSync}=require('child_process');
const assert=require('assert');
const candidate=process.argv[2];
if(!candidate) throw Error('usage: node frozen_alpha_ci_pr_path_filter_oracle_v1.js <candidate.js>');
const root='research/r16/axiom-alpha-node-c1-adaptation-20261012/';
const source={repo:'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
 pinned_workflow_commit:'b7adbc05c0d6b92ab77dd1fc7370f02506bfb3d9',
 inventory_commit:'56c383b6675d47b61d1b35bb543d24a2d36de512',
 inventory_blob:'66a330dddee79726c2384421ec2ac940a53f1225',
 pr_number:231,pr_head:'a6a04f775d620e1e94cb1fd0ebcd16dfa4518c4d',
 changed_files:[root+'a.js',root+'b.md',root+'c.js'],workflows:[]};
for(let i=0;i<17;i++){
 let paths=null;
 if(i>=4 && i<12) paths=[i===4?'research/ix/**':i===5?'research/fundus/**':`research/r${i}/**`];
 source.workflows.push({path:`.github/workflows/audit-${i}.yml`,blob_sha:(i+1).toString(16).padStart(40,'0'),
 byte_length:100+i,pull_request:true,paths,paths_ignore:false,
 jobs:[{id:i<12?'validate':`other-${i}`,name:null}]});
}
const clone=x=>JSON.parse(JSON.stringify(x));
const cases=[['baseline',clone(source),'PASS',4],
 ['ix_match',(()=>{let x=clone(source);x.changed_files=['research/ix/x.md'];return x})(),'PASS',5],
 ['fundus_match',(()=>{let x=clone(source);x.changed_files=['research/fundus/x.md'];return x})(),'PASS',5],
 ['effective_name_override',(()=>{let x=clone(source);x.workflows[12].jobs[0].name='validate';return x})(),'PASS',5]];
for(const [name,mutate] of [
 ['wrong_repo',x=>x.repo='attacker/repo'],
 ['wrong_pin',x=>x.pinned_workflow_commit='0'.repeat(40)],
 ['duplicate_changed',x=>x.changed_files.push(x.changed_files[0])],
 ['traversal',x=>x.changed_files=['../escape']],
 ['duplicate_workflow',x=>x.workflows[1].path=x.workflows[0].path],
 ['bad_blob',x=>x.workflows[0].blob_sha='x'.repeat(40)],
 ['missing_workflow',x=>x.workflows.pop()],
 ['unsupported_glob',x=>x.workflows[4].paths=['foo/[ab]']],
 ['unsupported_star',x=>x.workflows[4].paths=['foo/*.md']],
 ['missing_jobs',x=>x.workflows[0].jobs=[]],
 ['duplicate_job',x=>x.workflows[0].jobs.push({id:'validate',name:null})],
 ['bad_name',x=>x.workflows[0].jobs[0].name=123],
 ['bad_paths',x=>x.workflows[4].paths=[]],
 ['bad_ignore',x=>x.workflows[4].paths_ignore=true],
 ['malformed_changed',x=>x.changed_files=['a//b']]
]){let x=clone(source);mutate(x);cases.push([name,x,'FAIL_CLOSED',null]);}
let passed=0;
for(const [name,data,expected,count] of cases){
 const p=spawnSync(process.execPath,[candidate],{input:JSON.stringify(data),encoding:'utf8',timeout:5000,maxBuffer:1048576});
 if(p.error)throw p.error;
 let got;try{got=JSON.parse(p.stdout);}catch(e){throw Error(`${name}: non-JSON response ${p.stdout}`);}
 assert.strictEqual(got.status,expected,`${name}: wrong status`);
 assert.strictEqual(p.status,expected==='PASS'?0:2,`${name}: wrong exit code`);
 if(count!==null)assert.strictEqual(got.eligible,count,`${name}: wrong eligible count`);
 passed++;
}
const bad=spawnSync(process.execPath,[candidate],{input:'{"x":',encoding:'utf8',timeout:5000});
assert.strictEqual(bad.status,2);assert.strictEqual(JSON.parse(bad.stdout).status,'FAIL_CLOSED');passed++;
process.stdout.write(JSON.stringify({oracle:'FROZEN_BLACK_BOX',pass:passed,total:cases.length+1,negative:cases.length-4+1})+'\n');
