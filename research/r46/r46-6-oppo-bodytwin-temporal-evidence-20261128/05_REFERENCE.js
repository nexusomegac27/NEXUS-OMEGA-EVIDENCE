// R46-6 synthetic diagnostics only.
function run(){
 let seed=46606;const U=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return(seed+.5)/4294967296},Z=()=>Math.sqrt(-2*Math.log(U()))*Math.cos(2*Math.PI*U());
 const eq=(x,y)=>Math.abs(x-y)<1e-10,t=[0,1,2,3,4],omega=2,d=.03,phase=.4;
 const y=t.map(s=>phase+omega*(s+d)),y2=t.map(s=>phase+omega*d+omega*s);
 const a=.8,q=t.map(s=>phase+.5*a*(s+d)**2-.5*a*s*s),dhat=(q[4]-q[0])/(a*4);
 const clocks=[{offset:10,skew:1},{offset:10,skew:1.0001}];const anchor0=clocks.map(m=>m.offset),anchor100=clocks.map(m=>m.offset+100*m.skew);
 const worlds=[{offset:0,forward:10,reverse:10},{offset:8,forward:2,reverse:18}].map(m=>({...m,t:[0,m.forward+m.offset,m.forward+m.offset+2,m.forward+2+m.reverse]}));
 function replay(rows){let x=0,P=1,last=0;for(let r of rows){let t=Math.max(last,r.t);P+=t-last;const K=P/(P+1);x+=K*(r.z-x);P*=1-K;last=t}return {x,P}}
 const ev=[{t:1,z:1},{t:2,z:3}],ordered=replay(ev),arrival=replay([...ev].reverse());
 const N=100,M=6000,rho=.7,fac=1+2*Array.from({length:N-1},(_,i)=>(1-(i+1)/N)*rho**(2*(i+1))).reduce((s,v)=>s+v,0);let sum=0,sq=0,si=0,qi=0;
 for(let j=0;j<M;j++){let z=Z(),v=0,w=0;for(let k=0;k<N;k++){if(k)z=rho*z+Math.sqrt(1-rho*rho)*Z();v+=z*z;w+=Z()**2}v/=N;w/=N;sum+=v;sq+=v*v;si+=w;qi+=w*w}
 const arVar=sq/M-(sum/M)**2,iidVar=qi/M-(si/M)**2;
 function age(n,e,ttl){if(!n||!e)return "UNKNOWN";if(n.some(v=>!Number.isFinite(v))||e.some(v=>!Number.isFinite(v))||n[0]>n[1]||e[0]>e[1])return "INVALID";let lo=n[0]-e[1],hi=n[1]-e[0];return hi<0?"INVALID_FUTURE":lo>=0&&hi<=ttl?"FRESH":lo>ttl?"STALE":"AMBIGUOUS"}
 const ages=[age([100,101],[90,91],15),age([100,101],[70,71],15),age([100,102],[85,87],15),age([100,101],[102,103],15),age(null,[1,2],15),age([2,1],[0,1],15)];
 const big=BigInt("9007199254740993")-BigInt("9007199254740992");
 const checks={constant_speed:y.every((v,i)=>eq(v,y2[i])),variable_speed:eq(dhat,d),one_anchor:anchor0[0]===anchor0[1]&&!eq(anchor100[0],anchor100[1]),two_anchors:eq((anchor100[1]-10)/100,1.0001),ntp:JSON.stringify(worlds[0].t)===JSON.stringify(worlds[1].t),replay:!eq(ordered.x,arrival.x),ar1_variance:Math.abs(arVar/(2*fac/N)-1)<.12,ns:big===1n&&Number("9007199254740993")===Number("9007199254740992"),age:JSON.stringify(ages)===JSON.stringify(["FRESH","STALE","AMBIGUOUS","INVALID_FUTURE","UNKNOWN","INVALID"])};
 if(!Object.values(checks).every(Boolean))throw Error(JSON.stringify(checks));return {checks,phase_offset:{y,y2,offset:d,absorbed_phase:phase+omega*d,quadratic_recovered:dhat},clock:{anchor0,anchor100,skew_example_ppm:100},ntp_worlds:worlds,replay:{ordered,arrival,scope:"late event naively processed at current time, not correct OOSM"},AR1:{N,M,rho,exact_variance_factor:fac,expected_iid_mean_var:2/N,expected_correlated_mean_var:2*fac/N,empirical_iid_mean:si/M,empirical_correlated_mean:sum/M,empirical_iid_var:iidVar,empirical_correlated_var:arVar,empirical_ratio:arVar/iidVar},ages,limits:"Known quadratic motion toy; clocks exact synthetic; four-timestamp fixed-rate toy; stationary Gaussian AR1 independent trajectories; no HAC implementation or physical proof, no formal gate credit."};
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));