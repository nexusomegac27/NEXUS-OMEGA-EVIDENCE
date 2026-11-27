// R46-4 deterministic synthetic design and sharp moment-bound witnesses.
function run(){
 const m=9.832738001091458,s=.009171945499113295,g=9.80665,d=m-g,t=Math.hypot(d,s),p=(1+d/t)/2;
 const moment=(x,w)=>{const a=x.reduce((r,v,i)=>r+v*w[i],0);return {mean:a,sd:Math.sqrt(x.reduce((r,v,i)=>r+w[i]*(v-a)**2,0)),meanAbs:x.reduce((r,v,i)=>r+w[i]*Math.abs(v-g),0)}};
 const lower=moment([m-s,m+s],[.5,.5]),upper=moment([g-t,g+t],[1-p,p]);
 const eq=(x,y)=>Math.abs(x-y)<1e-10;
 const e=[[1,0,0],[0,1,0],[0,0,1]],six=[...e,...e.map(v=>v.map(x=>-x))],one=Array.from({length:6},()=>[0,0,1]),planar=Array.from({length:6},(_,i)=>[Math.cos(i*Math.PI/3),Math.sin(i*Math.PI/3),0]),clustered=planar.map(v=>[.01*v[0],.01*v[1],Math.sqrt(1-.01**2)]),tetra=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]].map(v=>v.map(x=>x/Math.sqrt(3)));
 function rank(a){a=a.map(v=>[...v,1]);let r=0;for(let c=0;c<4;c++){let k=r;for(let i=r;i<a.length;i++)if(Math.abs(a[i][c])>Math.abs(a[k]?.[c]??0))k=i;if(k>=a.length||Math.abs(a[k][c])<1e-10)continue;[a[r],a[k]]=[a[k],a[r]];for(let i=r+1;i<a.length;i++){let q=a[i][c]/a[r][c];for(let j=c;j<4;j++)a[i][j]-=q*a[r][j]}r++;if(r===a.length)break}return r}
 const ranks={one:rank(one),planar:rank(planar),clustered:rank(clustered),tetra:rank(tetra),six:rank(six)};
 // Unknown common reference rotation leaves exact observations unchanged.
 const A=[[1.02,.01,-.02],[.005,.98,.015],[.01,-.005,1.01]],b=[.02,-.01,.03],q=.01,Q=[[Math.cos(q),-Math.sin(q),0],[Math.sin(q),Math.cos(q),0],[0,0,1]];
 const dot=(a,b)=>a.reduce((r,x,i)=>r+x*b[i],0),mv=(A,v)=>A.map(a=>dot(a,v)),ATQ=A.map(a=>mv(Q,a)),obs=(M,v)=>mv(M,v).map((x,i)=>x+b[i]);
 const residual=Math.max(...six.flatMap(v=>obs(A,v).map((x,i)=>Math.abs(x-obs(ATQ,mv(Q,v))[i]))));
 const delta=Math.sqrt(A.flatMap((v,i)=>v.map((x,j)=>(x-ATQ[i][j])**2)).reduce((a,b)=>a+b,0));
 const ratio=.30044844215811695*Math.sqrt(2/3)/.009171949489023268;
 const checks={lower_moments:eq(lower.mean,m)&&eq(lower.sd,s),lower_attained:eq(lower.meanAbs,d),upper_moments:eq(upper.mean,m)&&eq(upper.sd,s),upper_attained:eq(upper.meanAbs,t),support_nonnegative:g-t>0&&m-s>0,rank_one:ranks.one===1,rank_planar:ranks.planar===3,rank_clustered:ranks.clustered===3,rank_tetra:ranks.tetra===4,rank_six:ranks.six===4,rotation_gauge:residual<1e-12&&delta>1e-3,rms_ratio:eq(ratio,26.74623601675417)};
 if(!Object.values(checks).every(Boolean))throw Error("reference check failed");
 return {checks,lower,upper,lower_support:[m-s,m+s],upper_support:[g-t,g+t],upper_weights:[1-p,p],ranks,rotation:{residual,delta},ratio,limits:"Moment-class bounds conditional on empirical population moments (not exact finite equal-weight extremizers or CI); normalized known-vector affine rank only; numeric tolerance explicit; synthetic not actual device; no formal credit."}
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
