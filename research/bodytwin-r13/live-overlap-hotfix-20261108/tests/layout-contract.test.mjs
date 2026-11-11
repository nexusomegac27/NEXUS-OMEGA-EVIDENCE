import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const script = fs.readFileSync(new URL('../site/layout-hotfix-r0.js', import.meta.url),'utf8');
const css = fs.readFileSync(new URL('../site/layout-hotfix-r0.css', import.meta.url),'utf8');
class Elem {
  constructor(tagName,id='') { this.tagName=tagName.toUpperCase(); this.id=id; this.children=[]; this.parentNode=null; this.dataset={}; }
  get nextSibling(){ if(!this.parentNode)return null; const i=this.parentNode.children.indexOf(this);return this.parentNode.children[i+1]||null; }
  append(child){return this.insertBefore(child,null);}
  insertBefore(child,ref){
    if(ref && !this.children.includes(ref))throw Error('REFERENCE_NOT_CHILD');
    if(ref===child)return child;
    if(child.parentNode){const i=child.parentNode.children.indexOf(child);if(i>=0)child.parentNode.children.splice(i,1);}
    child.parentNode=this;
    const j=ref?this.children.indexOf(ref):this.children.length;
    this.children.splice(j,0,child);
    return child;
  }
}
function setup({existing=true,duplicate=false,mainPresent=true,footerPresent=true}={}){
 const root=new Elem('html'),body=new Elem('body'),main=mainPresent?new Elem('main','bodytwin-main'):null;
 const viewer=new Elem('section','viewer'),controls=new Elem('div','viewer-controls'),footer=footerPresent?new Elem('footer','footer'):null;
 if(main){main.append(viewer);main.append(controls);body.append(main);}
 if(footer)body.append(footer);
 const panel=existing?new Elem('section','nexus-bodytwin-live-c1'):null;
 if(panel)(main||body).append(panel);
 if(duplicate)(main||body).append(new Elem('section','nexus-bodytwin-live-c1'));
 const observers=[],events={};
 function visit(node,id,out){if(node.id===id)out.push(node);for(const c of node.children)visit(c,id,out);}
 const document={documentElement:root,body,
  querySelector(q){if(q==='main')return main;return null;},
  querySelectorAll(q){const found=[];visit(body,q.slice(1),found);return found;},
  addEventListener(n,fn){events[n]=fn;}
 };
 const window={addEventListener(n,fn){events[n]=fn;}};
 class MutationObserver{constructor(fn){this.fn=fn;observers.push(this);}observe(){this.active=true;}disconnect(){this.active=false;}}
 function run(){vm.runInNewContext(script,{document,window,MutationObserver},{timeout:1000});}
 function trigger(){for(const o of observers)if(o.active)o.fn();}
 return {root,body,main,viewer,controls,footer,panel,document,window,observers,events,run,trigger};
}
test('existing panel moved OUTSIDE main into its following sibling slot',()=>{let d=setup();d.run();assert.equal(d.panel.parentNode,d.body);assert.equal(d.main.nextSibling,d.panel);assert.equal(d.panel.nextSibling,d.footer)});
test('4D original main children and identity preserved',()=>{let d=setup();d.run();assert.deepEqual(d.main.children,[d.viewer,d.controls]);assert.equal(d.viewer.parentNode,d.main);assert.equal(d.controls.parentNode,d.main)});
test('layout isolated status observable in DOM',()=>{let d=setup();d.run();assert.equal(d.root.dataset.nexusBodytwinLayout,'PASS_ISOLATED_PANEL');assert.equal(d.panel.dataset.layoutFix,'isolated')});
test('idempotent second invocation, not duplicated',()=>{let d=setup();d.run();d.run();assert.equal(d.document.querySelectorAll('#nexus-bodytwin-live-c1').length,1);assert.deepEqual(d.body.children,[d.main,d.panel,d.footer])});
test('no main: place before root footer, keep content',()=>{let d=setup({mainPresent:false});d.run();assert.equal(d.panel.parentNode,d.body);assert.equal(d.panel.nextSibling,d.footer)});
test('main with no footer: append after main',()=>{let d=setup({footerPresent:false});d.run();assert.deepEqual(d.body.children,[d.main,d.panel])});
test('late panel mounting by original module repaired via observer',()=>{let d=setup({existing:false});d.run();assert.equal(d.observers.length,1);d.panel=new Elem('section','nexus-bodytwin-live-c1');d.main.append(d.panel);d.trigger();assert.equal(d.main.nextSibling,d.panel);assert.equal(d.observers[0].active,false)});
test('duplicate ID is a visible HARD HOLD, never silently removes modules',()=>{let d=setup({duplicate:true});d.run();assert.equal(d.root.dataset.nexusBodytwinLayout,'HOLD_DUPLICATE_PANEL');assert.equal(d.document.querySelectorAll('#nexus-bodytwin-live-c1').length,2)});
test('no panel produces hold marker when load ends',()=>{let d=setup({existing:false});d.run();d.events.load();assert.equal(d.root.dataset.nexusBodytwinLayout,'HOLD_PANEL_NOT_FOUND')});
test('only panel-scoped CSS, no viewer selectors changed',()=>{assert.match(css,/#nexus-bodytwin-live-c1/);assert.doesNotMatch(css,/(^|\n)\s*(body|main|canvas|\.viewer)\s*\{/);});
test('grid/flex/position are isolated',()=>{for(const s of ['grid-column: 1 / -1','position: relative','min-width: 0','clear: both','max-width: 1180px'])assert.ok(css.includes(s),s)});
test('mobile adaptation exists',()=>{assert.ok(css.includes('@media (max-width: 640px)'));assert.ok(css.includes('width: calc(100% - 16px)'))});
test('no new network, timers, sensor or personal-data reads',()=>{for(const s of ['fetch(', 'XMLHttpRequest','setInterval(', 'navigator.mediaDevices','navigator.sensors','localStorage','sessionStorage','sendBeacon','WebSocket','getUserMedia'])assert.equal(script.includes(s),false,s)});
test('does not mutate textContent or any live C1 data fields',()=>{for(const s of ['textContent','source_changed','producer','validated','consent','trial','A72','current.json'])assert.equal(script.includes(s),false,s)});
test('script is syntax-valid in isolated JS context',()=>{assert.doesNotThrow(()=>new vm.Script(script))});
