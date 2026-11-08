import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const src=fs.readFileSync(new URL('../q0-reference/viewer.js',import.meta.url),'utf8');
const calls=[];const elements=new Map();const elem=id=>{if(!elements.has(id))elements.set(id,{id,value:'perspective',textContent:'',appendChild(x){this.children??=[];this.children.push(x)},addEventListener(){},getContext(){return {clearRect(){},beginPath(){},moveTo(x,y){calls.push(['moveTo',x,y])},lineTo(x,y){calls.push(['lineTo',x,y])},stroke(){}}},width:800,height:600});return elements.get(id)};
const sandbox={document:{getElementById:elem,createElement:()=>({appendChild(){},addEventListener(){}}),querySelectorAll:()=>[]},requestAnimationFrame:()=>{},setInterval:()=>{},fetch:async()=>({ok:false}) ,console};
vm.runInNewContext(src+'\n;globalThis.__x={vertices,edges,applySO4,project,toScreen,draw,angles};',sandbox,{timeout:2000});
const {vertices,edges,applySO4,project,toScreen,draw,angles}=sandbox.__x;
const checks=[];function test(name,fn){try{fn();checks.push({name,pass:true})}catch(err){checks.push({name,pass:false,error:String(err)})}}
const eq=(a,b,tol=1e-9)=>{assert.equal(a.length,b.length);for(let i=0;i<a.length;i++) assert.ok(Math.abs(a[i]-b[i])<=tol,`${a[i]} != ${b[i]}`)};
test('16 unique 4D vertices',()=>{assert.equal(vertices.length,16);assert.equal(new Set(vertices.map(x=>x.join(','))).size,16)});
test('32 unique bit-adjacent edges',()=>{assert.equal(edges.length,32);for(const [i,j] of edges)assert.equal(vertices[i].filter((v,k)=>v!==vertices[j][k]).length,1)});
test('6 plane rotation controls source',()=>{for(const p of ['XY','XZ','XW','YZ','YW','ZW'])assert.ok(src.includes("['"+p+"'"))});
test('5 projection modes source',()=>{for(const mode of ['perspective','orthographic','stereographic','schlegel','double-perspective'])assert.ok(src.includes("case '"+mode+"'"))});
test('identity rotation all vertices',()=>{for(const v of vertices)eq(applySO4(v,{XY:0,XZ:0,XW:0,YZ:0,YW:0,ZW:0}),v)});
test('plane rotations preserve 4D norm',()=>{for(const plane of Object.keys(angles)) {const a={...angles,[plane]:1.237};for(const v of vertices){const w=applySO4(v,a);const n=v.reduce((s,x)=>s+x*x,0),m=w.reduce((s,x)=>s+x*x,0);assert.ok(Math.abs(m-n)<1e-12)}}});
test('orthographic drops W',()=>eq(project([1,2,3,.5],'orthographic'),[1,2,3]));
test('perspective nominal finite',()=>{const out=project([1,2,0,.1],'perspective');assert.ok(out.every(Number.isFinite))});
test('stereographic nominal finite',()=>{const out=project([1,2,0,.1],'stereographic');assert.ok(out.every(Number.isFinite))});
test('schlegel nominal finite',()=>{const out=project([1,2,0,.1],'schlegel');assert.ok(out.every(Number.isFinite))});
test('double-perspective nominal finite',()=>{const out=project([1,2,.2,.1],'double-perspective');assert.ok(out.every(Number.isFinite))});
test('negative: perspective pole rejected',()=>{const out=project([1,1,1,3],'perspective');assert.ok(out.every(Number.isFinite),'nonfinite accepted')});
test('negative: schlegel pole rejected',()=>{const out=project([1,1,1,2],'schlegel');assert.ok(out.every(Number.isFinite),'nonfinite accepted')});
test('negative: double perspective Z pole rejected',()=>{const out=project([1,1,3,0],'double-perspective');assert.ok(out.every(Number.isFinite),'nonfinite accepted')});
test('negative: stereo pole fails closed instead of silent orthographic',()=>{const out=project([1,2,3,1],'stereographic');assert.ok(out.every(Number.isFinite));assert.notDeepEqual(Array.from(out),[1,2,3],'silently substitutes orthographic geometry')});
test('negative: invalid nonfinite angle must reject',()=>{const out=applySO4([1,2,3,4],{...angles,XY:NaN});assert.ok(out.every(Number.isFinite),'nonfinite accepted')});
test('negative: any nonfinite screen coordinate rejected',()=>{const p=toScreen([1,Infinity,0]);assert.ok(p.every(Number.isFinite),'nonfinite y accepted')});
test('negative: drawing rejects nonfinite y',()=>{calls.length=0;elem('projection-mode').value='perspective';draw();for(const call of calls)for(const v of call.slice(1))assert.ok(Number.isFinite(v))});
const pass=checks.filter(x=>x.pass).length;console.log(JSON.stringify({object:'NEXUS_OMEGA_AXIOM_Q0_RECONSTRUCTED_VIEWER_INDEPENDENT_TESTS_20261108_R0',node:process.version,pass,total:checks.length,failed:checks.filter(x=>!x.pass),claims:'RECONSTRUCTED_REFERENCE_ONLY_NOT_PRODUCTION'},null,2));
if(checks.some(x=>!x.pass)) process.exitCode=1; // EXPECTED failure on uncorrected reconstructed reference; do not hide counterexamples
