/* R11 / Forum GitHub Implant C1 source freshness regression fixtures.
 * Node 22 built-in test, no network; fake GitHub API.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";
const source=readFileSync(new URL("../site/assets/github-implant.js", import.meta.url),"utf8");
function harness({prHttp=200}={}) {
  const nodes=new Map(),calls=[];let interval=null;
  function element(tag="") {
    return {tag,id:tag,className:"",hidden:false,disabled:false,textContent:"",value:"",
      children:[],attributes:{},style:{},append(...items){this.children.push(...items)},
      replaceChildren(...items){this.children=items},addEventListener(){},
      setAttribute(k,v){this.attributes[k]=v},focus(){}};
  }
  const document={
    hidden:false,
    getElementById(id){if(!nodes.has(id))nodes.set(id,element(id));return nodes.get(id)},
    createElement:element,querySelectorAll(){return []}
  };
  async function fetch(url,options={}) {
    calls.push({url:String(url),method:options.method||"GET"});
    if(String(url).includes("/commits?"))return {
      ok:true,status:200,headers:{get(){return null}},json:async()=>[{
        sha:"d355400dabed3c280e1fce5030cab69ea099428b",
        html_url:"https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/commit/d355400dabed3c280e1fce5030cab69ea099428b",
        commit:{message:"Unchanged Main",committer:{date:"2026-10-13T03:42:25Z"},author:{name:"source"}}
      }]
    };
    if(String(url).includes("/pulls?"))return {
      ok:prHttp===200,status:prHttp,headers:{get(){return null}},json:async()=>[{
        number:115,state:"open",merged_at:null,title:"R10 source",
        html_url:"https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/115",
        updated_at:"2026-10-16T07:40:00Z"
      }]
    };
    throw new Error("unexpected URL "+url);
  }
  vm.runInNewContext(source,{document,fetch,URL,Date,Intl,AbortController,
    setInterval(fn,ms){interval={fn,ms};return 1},setTimeout(){return 1},clearTimeout(){}},
    {timeout:1500});
  return {document,nodes,calls,get interval(){return interval},value:id=>document.getElementById(id).textContent};
}
const settle=async()=>{for(let i=0;i<4;i++)await new Promise(resolve=>setImmediate(resolve))};
test("separate older main and more recent PR activity are both shown",async()=>{
  const h=harness();await settle();
  assert.equal(h.value("head-short"),"d355400dab");
  assert.match(h.value("pr-activity"),/PR #115/);
  assert.match(h.value("pr-activity"),/PR-Aktivität ist kein Main-Commit/);
  assert.deepEqual(h.calls.map(c=>c.url.includes("/pulls?")?"pulls":"commits"),["commits","pulls"]);
});
test("PR API failure does not invent latest activity",async()=>{
  const h=harness({prHttp:403});await settle();
  assert.match(h.value("pr-activity"),/nicht abrufbar/);
  assert.doesNotMatch(h.value("pr-activity"),/PR #115/);
});
test("five-minute read-only poll only runs when visible",async()=>{
  const h=harness();await settle();
  assert.equal(h.interval.ms,300000);
  assert.ok(h.calls.every(c=>c.method==="GET"));
  const before=h.calls.length;h.document.hidden=true;h.interval.fn();await settle();
  assert.equal(h.calls.length,before);
  h.document.hidden=false;h.interval.fn();await settle();
  assert.ok(h.calls.every(c=>c.method==="GET"));
});
