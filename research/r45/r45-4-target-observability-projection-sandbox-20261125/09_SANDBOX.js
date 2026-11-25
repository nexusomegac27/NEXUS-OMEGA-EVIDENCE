// Independent implementation, standard JS only. No IO except stdout under Node.
function run(){
 const G=[new Map(),new Map(),new Map()], S=[], coords=Array.from({length:16},(_,k)=>[k>>2,k%4]);
 function observation(m){let v=Array(22).fill(0),t=0,p=(m>>5)&1;for(let k=0;k<16;k++)if((m>>k)&1){let [i,j]=coords[k];v[i]++;v[4+j]++;v[8+i+j]++;v[18+i-j]++;if(i>=1&&i<=2&&j>=1&&j<=2)t++}return {v,t,p,m}}
 let pair=null;
 for(let m=0;m<65536;m++){let x=observation(m);for(let l=0;l<3;l++){let key=x.v.slice(0,[8,15,22][l]).join(","),g=G[l],a=g.get(key);if(a){if(l===2&&!pair)pair=[a.first,m];a.n++;a.lo=Math.min(a.lo,x.t);a.hi=Math.max(a.hi,x.t)}else g.set(key,{n:1,lo:x.t,hi:x.t,first:m})}if(x.v.slice(0,8).every(k=>k===2))S.push(x)}
 const levels=G.map(g=>{let r={fibers:g.size,singleton_states:0,target_identified_states:0,max_target_width:0,largest_fiber:0};for(let x of g.values()){if(x.n===1)r.singleton_states++;if(x.lo===x.hi)r.target_identified_states+=x.n;r.max_target_width=Math.max(r.max_target_width,x.hi-x.lo);r.largest_fiber=Math.max(r.largest_fiber,x.n)}return r});
 const views={sum_diag:x=>x.v.slice(8,15),diff_diag:x=>x.v.slice(15),central_pixel:x=>[x.p],target_sum:x=>[x.t],both_diags:x=>x.v.slice(8)};
 const dist=(a,b)=>Math.max(...a.map((x,i)=>Math.abs(x-b[i])));
 const W={};for(let [name,view] of Object.entries(views)){const calc=eps=>{let ws=S.map(x=>{let ts=S.filter(y=>dist(view(x),view(y))<=eps).map(y=>y.t);return Math.max(...ts)-Math.min(...ts)});let robust=0,witness=null;for(let x of S)for(let y of S)if(dist(view(x),view(y))<=2*eps&&Math.abs(x.t-y.t)>robust){robust=Math.abs(x.t-y.t);witness=[x.m,y.m]}return {max:Math.max(...ws),mean:ws.reduce((a,b)=>a+b,0)/ws.length,identified:ws.filter(x=>x===0).length,robust_all_observations:robust,witness}};W[name]={exact:calc(0),bounded_1:calc(1),bounded_2:calc(2)}}
 const w=[3,2,1,0,0,0,0,0,-3,-2,-1,0,0,0,0,-3,-2,-1,0,0,0,0],n=[0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0];
 const cols=coords.map(([i,j],k)=>observation(1<<k).v);
 const c=coords.map(([i,j])=>+(i>=1&&i<=2&&j>=1&&j<=2));
 const dot=(a,b)=>a.reduce((s,v,k)=>s+v*b[k],0);
 const cert=cols.every((v,k)=>dot(v,w)===c[k]),nullOK=w.every((_,j)=>cols.reduce((a,v,k)=>a+v[j]*n[k],0)===0)&&dot(c,n)===0;
 const vox=[[],[]];for(let i=0;i<2;i++)for(let j=0;j<2;j++)for(let k=0;k<2;k++)vox[(i+j+k)%2].push([i,j,k]);const ray=(v,a)=>v.map(x=>x.filter((_,i)=>i!==a).join(",")).sort().join(";");
 const parity=[0,1,2].every(a=>ray(vox[0],a)===ray(vox[1],a));
 // Exact rational count units 1/100: q allocated symmetrically by count.
 const collective=[0,4].map(t=>{let q=[52-t,36+3*t,12-3*t,t];return {q, marginal_numerator_over_300:q[1]+2*q[2]+3*q[3],pair_numerator_over_600:2*q[2]+6*q[3],majority_percent:q[2]+q[3]}});
 if(!cert||!nullOK||!parity||levels[2].target_identified_states!==65536||collective.some(x=>x.marginal_numerator_over_300!==60||x.pair_numerator_over_600!==24))throw Error("contract failure");
 return {levels,selected_count:S.length,views:W,first_four_view_pair:pair,certificate:cert,null_witness:nullOK,parity,collective,formal_credit:false};
}
const result=run();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
