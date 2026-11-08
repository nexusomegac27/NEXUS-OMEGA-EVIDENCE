/* NEXUS OMEGA R18 / C1: additive, read-only, browser-only WebGL visualization.
 * R17.1 original data layers are transported byte-identically; no feed or SO(4) mutation.
 * Hologram is a rendering effect, not a geometric/measured dimension or physical laser.
 */
(()=>{
'use strict';
const keys=['skeleton','muscles','organs_male','organs_female'];
const $=id=>document.getElementById(id);
const canvas=$('c');
const status=$('runtime-state'), sceneStatus=$('render-status'), stats=$('mesh-stats'), fallback=$('fallback');
const limits=window.NEXUS_R18_JOINT_LIMITS||[];
const modelState={skeleton:true,muscles:true,organs_male:false,organs_female:false,mode:'reference'};
const loadPromises=new Map();
const layers=Object.create(null);
let gl,prog,loc; let animating=false,invalidated=false,frameRequested=false,lastFrame=0;
const camera={th:0,ph:0.08,r:2650,tgt:[0,0,950]};
function visibleFailure(message){
  fallback.textContent=''; fallback.hidden=false;
  const caption=document.createElement('p'); caption.textContent=message+' · Statischer, quellgebundener R17.1-Screenshot (kein Echtzeit-Rendering).';
  const screenshot=document.createElement('img'); screenshot.alt='R17.1 statische anatomische Referenz (nicht medizinisch validiert)';
  screenshot.src='fallback/assembly_02_skeleton_muscles.png';screenshot.id='fallback-screenshot';
  fallback.append(screenshot,caption);sceneStatus.textContent='Statische Fallback-Referenz';status.textContent='ANZEIGE_FAIL_CLOSED · STATIC_FALLBACK';
  ['l-skeleton','l-muscles','mode-ref','mode-holo','reset-camera'].forEach(id=>{$(id).disabled=true;});
  document.querySelectorAll('input[name="organs"]').forEach(input=>input.addEventListener('change',()=>{
    const selected=document.querySelector('input[name="organs"]:checked').value;
    screenshot.src=selected==='organs_male'?'fallback/assembly_03_with_organs_male.png':
      selected==='organs_female'?'fallback/assembly_04_with_organs_female.png':'fallback/assembly_02_skeleton_muscles.png';
  }));
}
function renderLimits(){
 const tbody=document.querySelector('#limits-table tbody');
 for(const l of limits){const tr=document.createElement('tr');
   for(const v of [l.name,l.min,l.max,l.unit]){const td=document.createElement('td');td.textContent=String(v);tr.append(td);}tbody.append(tr);}
}
renderLimits();
const VERTEX=`attribute vec3 p;attribute vec3 n;uniform mat4 mvp;uniform mat3 nm;varying vec3 vn;varying vec3 vp;
void main(){vp=p;vn=normalize(nm*n);gl_Position=mvp*vec4(p,1.0);}`;
const FRAGMENT=`precision mediump float;varying vec3 vn;varying vec3 vp;uniform vec3 col;uniform vec3 eye;
uniform float uTime;uniform float uHologram;
void main(){
 vec3 n=normalize(vn);vec3 viewDir=normalize(eye-vp);
 vec3 l1=normalize(vec3(-0.4,-0.7,0.8));vec3 l2=normalize(vec3(0.5,0.4,-0.6));
 float d=0.18+0.55*max(dot(n,l1),0.0)+0.3*max(dot(n,l2),0.0);
 vec3 solid=col*(0.23+0.77*d)*(0.68+0.32*max(dot(n,viewDir),0.0));
 float rim=pow(1.0-max(dot(n,viewDir),0.0),2.6);
 float scan=0.54+0.46*sin(vp.z*0.054+uTime*2.3);
 vec3 laser=mix(vec3(0.018,0.21,0.27),col*vec3(0.24,0.95,1.18),0.55)+vec3(0.07,0.63,0.75)*rim;
 vec3 holo=laser*(0.5+0.5*scan)+vec3(0.02,0.26,0.3)*rim;
 gl_FragColor=vec4(mix(solid,holo,step(0.5,uHologram)),1.0);
}`;
function shader(kind,source){const s=gl.createShader(kind);gl.shaderSource(s,source);gl.compileShader(s);
 if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){const error=gl.getShaderInfoLog(s);gl.deleteShader(s);throw Error(error);}return s;}
function initWebGL(){
 gl=canvas.getContext('webgl2',{antialias:true,alpha:false,depth:true,powerPreference:'low-power'}) ||
    canvas.getContext('webgl',{antialias:true,alpha:false,depth:true,powerPreference:'low-power'});
 if(!gl) throw Error('WebGL ist auf diesem Gerät oder Browser nicht verfügbar. Die Originalansicht bleibt unverändert.');
 if(!(typeof WebGL2RenderingContext!=='undefined' && gl instanceof WebGL2RenderingContext) && !gl.getExtension('OES_element_index_uint'))
   throw Error('Dieser WebGL-1-Browser unterstützt keine 32-Bit-Geometrieindizes. Kein unsicherer Fallback.');
 const vs=shader(gl.VERTEX_SHADER,VERTEX),fs=shader(gl.FRAGMENT_SHADER,FRAGMENT);
 prog=gl.createProgram();gl.attachShader(prog,vs);gl.attachShader(prog,fs);gl.linkProgram(prog);
 if(!gl.getProgramParameter(prog,gl.LINK_STATUS)) throw Error(gl.getProgramInfoLog(prog));
 gl.useProgram(prog);loc={p:gl.getAttribLocation(prog,'p'),n:gl.getAttribLocation(prog,'n'),
  mvp:gl.getUniformLocation(prog,'mvp'),nm:gl.getUniformLocation(prog,'nm'),col:gl.getUniformLocation(prog,'col'),
  eye:gl.getUniformLocation(prog,'eye'),time:gl.getUniformLocation(prog,'uTime'),mode:gl.getUniformLocation(prog,'uHologram')};
 gl.enable(gl.DEPTH_TEST);gl.enableVertexAttribArray(loc.p);gl.enableVertexAttribArray(loc.n);
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();animating=false;visibleFailure('WebGL-Kontext verloren. Seite neu laden; die Hauptansicht bleibt unberührt.');});
}
function decode(b64,T){const binary=atob(b64),out=new Uint8Array(binary.length);
 for(let i=0;i<binary.length;i++) out[i]=binary.charCodeAt(i);
 if(out.byteLength%T.BYTES_PER_ELEMENT) throw Error('Ungültige Geometrielänge');
 return new T(out.buffer);}
function hex2rgb(hex){if(!/^#[0-9A-Fa-f]{6}$/.test(hex))throw Error('Ungültiger Farbwert');return [1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255);}
function attachLayer(key){
 const packet=window.R17_ASSEMBLY?.layers?.[key];
 if(!packet||!Array.isArray(packet.meshes)) throw Error('Geometrielayer fehlt: '+key);
 const P=decode(packet.positions_b64,Float32Array),N=decode(packet.normals_b64,Float32Array),I=decode(packet.indices_b64,Uint32Array);
 if(P.length%3 || N.length!==P.length || I.length%3)throw Error('Geometrische Struktur inkonsistent: '+key);
 if(!P.every(Number.isFinite) || !N.every(Number.isFinite))throw Error('Nichtendliche Geometrie: '+key);
 for(let i=0;i<I.length;i++)if(I[i]*3>=P.length)throw Error('Index außerhalb Geometrie: '+key);
 const buffers=[];
 function upload(kind,arr){let b=gl.createBuffer();if(!b)throw Error('GPU-Bufferspeicher nicht verfügbar');
   buffers.push(b);gl.bindBuffer(kind,b);gl.bufferData(kind,arr,gl.STATIC_DRAW);if(gl.getError()!==gl.NO_ERROR)throw Error('GPU-Upload fehlgeschlagen');return b;}
 let vb,nb,ib;
 try{vb=upload(gl.ARRAY_BUFFER,P);nb=upload(gl.ARRAY_BUFFER,N);ib=upload(gl.ELEMENT_ARRAY_BUFFER,I);}catch(e){buffers.forEach(x=>gl.deleteBuffer(x));throw e;}
 const meshes=packet.meshes.map(m=>({color:hex2rgb(m.color),ii:m.ii,ic:m.ic}));
 for(const m of meshes)if(!Number.isInteger(m.ii)||!Number.isInteger(m.ic)||m.ic<0||m.ii<0||m.ii+m.ic>I.length)
    throw Error('Mesh-Grenzen inkonsistent: '+key);
 layers[key]={vb,nb,ib,meshes,triangles:I.length/3,structures:meshes.length};
 delete window.R17_ASSEMBLY.layers[key]; // large Base64 is not retained after GPU upload
 sceneStatus.textContent='WebGL-Layer geladen';updateStats();invalidate();
}
function unloadLayer(key){const l=layers[key];if(!l)return;[l.vb,l.nb,l.ib].forEach(b=>gl.deleteBuffer(b));delete layers[key];updateStats();invalidate();}
function loadLayer(key){
 if(!keys.includes(key))return Promise.reject(Error('Nicht freigegebener Layer'));
 if(layers[key])return Promise.resolve();
 if(loadPromises.has(key))return loadPromises.get(key);
 sceneStatus.textContent='Lade '+key+' …';
 const p=new Promise((resolve,reject)=>{let s=document.createElement('script');s.src='data/data_layer_'+key+'.js';s.async=true;
   s.onload=()=>{try{attachLayer(key);resolve();}catch(e){reject(e);}finally{s.remove();}};
   s.onerror=()=>{s.remove();reject(Error('Fehler beim Laden von '+key));};
   document.head.append(s);
 }).catch(e=>{sceneStatus.textContent='Layer-Fehler: '+key;status.textContent='TEILANSICHT · '+key+' nicht verfügbar';throw e;})
 .finally(()=>loadPromises.delete(key));loadPromises.set(key,p);return p;
}
function updateStats(){let structures=0,tris=0;for(const [k,l] of Object.entries(layers))if(modelState[k]){structures+=l.structures;tris+=l.triangles;}
 stats.textContent=`${structures.toLocaleString('de-DE')} dargestellte Strukturen · ${Math.round(tris).toLocaleString('de-DE')} Dreiecke · statische C1-Referenz`;
}
function sub(a,b){return[a[0]-b[0],a[1]-b[1],a[2]-b[2]];}
function cross(a,b){return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
function norm(a){const l=Math.hypot(...a)||1;return a.map(x=>x/l);}
function perspective(fovy,aspect,near,far){const q=1/Math.tan(fovy/2);return[q/aspect,0,0,0,0,q,0,0,0,0,(far+near)/(near-far),-1,0,0,2*far*near/(near-far),0];}
function lookAt(eye,target,up){const z=norm(sub(eye,target)),x=norm(cross(up,z)),y=cross(z,x);
 return [x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-dot(x,eye),-dot(y,eye),-dot(z,eye),1];}
function matmul(a,b){const result=new Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++){
 let v=0;for(let k=0;k<4;k++)v+=a[k*4+r]*b[c*4+k];result[c*4+r]=v;}return result;}
function camEye(){return[camera.tgt[0]+camera.r*Math.cos(camera.ph)*Math.sin(camera.th),
 camera.tgt[1]-camera.r*Math.cos(camera.ph)*Math.cos(camera.th),camera.tgt[2]+camera.r*Math.sin(camera.ph)];}
function resize(){const box=canvas.getBoundingClientRect();if(box.width<1||box.height<1)return;
 const dpr=Math.min(window.devicePixelRatio||1,window.innerWidth<740?1.2:1.7);
 const w=Math.max(1,Math.min(1800,Math.round(box.width*dpr))),h=Math.max(1,Math.min(1400,Math.round(box.height*dpr)));
 if(w!==canvas.width||h!==canvas.height){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h);invalidate();}}
function invalidate(){invalidated=true;if(!frameRequested){frameRequested=true;requestAnimationFrame(render);}}
function render(t){frameRequested=false;if(!gl||fallback.hidden===false)return;
 const holo=modelState.mode==='holo';if(!invalidated&&(!holo||t-lastFrame<50)){if(holo)invalidate();return;}
 lastFrame=t;invalidated=false;resize();gl.clearColor(0.026,0.061,0.081,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
 const eye=camEye(),mvp=matmul(perspective(.86,canvas.width/Math.max(canvas.height,1),3,200000),lookAt(eye,camera.tgt,[0,0,1]));
 gl.useProgram(prog);gl.uniformMatrix4fv(loc.mvp,false,new Float32Array(mvp));gl.uniformMatrix3fv(loc.nm,false,new Float32Array([1,0,0,0,1,0,0,0,1]));
 gl.uniform3fv(loc.eye,new Float32Array(eye));gl.uniform1f(loc.time,t/1000);gl.uniform1f(loc.mode,holo?1:0);
 for(const key of keys){const l=layers[key];if(!l||!modelState[key])continue;
   gl.bindBuffer(gl.ARRAY_BUFFER,l.vb);gl.vertexAttribPointer(loc.p,3,gl.FLOAT,false,0,0);
   gl.bindBuffer(gl.ARRAY_BUFFER,l.nb);gl.vertexAttribPointer(loc.n,3,gl.FLOAT,false,0,0);
   gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,l.ib);
   for(const m of l.meshes){gl.uniform3fv(loc.col,new Float32Array(m.color));gl.drawElements(gl.TRIANGLES,m.ic,gl.UNSIGNED_INT,m.ii*4);}
 }
 if(holo&&!document.hidden)invalidate();
}
function setMode(mode){modelState.mode=mode;for(const choice of ['ref','holo']){
 const b=$('mode-'+choice),active=(choice==='ref'&&mode==='reference'||choice==='holo'&&mode==='holo');
 b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));}invalidate();}
function bindEvents(){
 for(const key of ['skeleton','muscles']){$('l-'+key).addEventListener('change',async e=>{
 modelState[key]=e.target.checked;updateStats();invalidate();if(modelState[key])try{await loadLayer(key);}catch(err){console.error(err);}});}
 document.querySelectorAll('input[name="organs"]').forEach(input=>input.addEventListener('change',async()=>{
  const selected=document.querySelector('input[name="organs"]:checked').value;
  modelState.organs_male=selected==='organs_male';modelState.organs_female=selected==='organs_female';
  const off=selected==='organs_male'?'organs_female':'organs_male';unloadLayer(off);
  if(selected==='none'){unloadLayer('organs_male');unloadLayer('organs_female');}
  else try{await loadLayer(selected);if(!modelState[selected])unloadLayer(selected);}catch(err){console.error(err);}
  updateStats();invalidate();
 }));
 $('mode-ref').addEventListener('click',()=>setMode('reference'));
 $('mode-holo').addEventListener('click',()=>setMode('holo'));
 $('reset-camera').addEventListener('click',()=>{Object.assign(camera,{th:0,ph:0.08,r:2650,tgt:[0,0,950]});invalidate();});
 let drag=null;const pointers=new Map();
 canvas.addEventListener('pointerdown',e=>{canvas.setPointerCapture(e.pointerId);pointers.set(e.pointerId,[e.clientX,e.clientY]);
  if(pointers.size===1)drag={x:e.clientX,y:e.clientY,shift:e.shiftKey||e.button===2};});
 canvas.addEventListener('pointerup',e=>{pointers.delete(e.pointerId);if(!pointers.size)drag=null;});
 canvas.addEventListener('pointercancel',e=>{pointers.delete(e.pointerId);drag=null;});
 canvas.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;
  if(pointers.size>1){const old=[...pointers.values()];pointers.set(e.pointerId,[e.clientX,e.clientY]);const next=[...pointers.values()];
    const prevDist=Math.hypot(old[0][0]-old[1][0],old[0][1]-old[1][1]);
    const nextDist=Math.hypot(next[0][0]-next[1][0],next[0][1]-next[1][1]);
    if(nextDist>5&&prevDist>5)camera.r=Math.max(350,Math.min(16000,camera.r*prevDist/nextDist));invalidate();return;}
  if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;pointers.set(e.pointerId,[e.clientX,e.clientY]);
  drag.x=e.clientX;drag.y=e.clientY;
  if(drag.shift){const scale=camera.r*0.0017;camera.tgt[0]-=dx*Math.cos(camera.th)*scale;camera.tgt[1]+=dx*Math.sin(camera.th)*scale;camera.tgt[2]+=dy*scale;}
  else{camera.th-=dx*0.006;camera.ph=Math.max(-1.45,Math.min(1.45,camera.ph+dy*0.006));}invalidate();});
 canvas.addEventListener('contextmenu',e=>e.preventDefault());
 canvas.addEventListener('wheel',e=>{e.preventDefault();camera.r=Math.max(350,Math.min(16000,camera.r*(e.deltaY>0?1.11:.9)));invalidate();},{passive:false});
 window.addEventListener('resize',resize);document.addEventListener('visibilitychange',invalidate);
 if('ResizeObserver' in window)new ResizeObserver(resize).observe(canvas);
}
async function start(){
 try{initWebGL();bindEvents();resize();invalidate();
  await loadLayer('skeleton');await loadLayer('muscles');
  status.textContent='REFERENZBEREIT · Live-Feed getrennt';sceneStatus.textContent='Statische T-Pose · kein Sensorbetrieb';updateStats();}
 catch(err){console.error(err);visibleFailure('Die anatomische Ansicht wurde sicher angehalten: '+err.message);}
}
start();
})();
