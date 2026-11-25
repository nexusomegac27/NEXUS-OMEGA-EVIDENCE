// New isolated reference, no I/O or runtime authority.
function bounds(p) {
 if (!p.length || p.some(x=>!Number.isFinite(x)||x<0||x>1)) throw Error("invalid marginals");
 return [Math.max(0,p.reduce((a,b)=>a+b,0)-p.length+1),Math.min(...p)];
}
function validAck(now,issued,ttl,last,epoch,ackEpoch) {
 return [now,issued,ttl,last,epoch,ackEpoch].every(Number.isSafeInteger) &&
 ttl>=0 && now>=last && now>=issued && now-issued<=ttl && epoch===ackEpoch;
}
function test() {
 const x=[0,0],y=[1,-1],sum=a=>a.reduce((p,q)=>p+q,0),norm2=a=>a.reduce((p,q)=>p+q*q,0);
 if(sum(x)!==sum(y)||norm2(x)===norm2(y)) throw Error("witness");
 const [lo,hi]=bounds([.95,.95,.95,.95]); if(Math.abs(lo-.8)>1e-12||hi!==.95)throw Error("bounds");
 let n=0;
 for (let now=0;now<=4;now++)for(let issued=0;issued<=4;issued++)for(let last=0;last<=4;last++)for(let epoch=0;epoch<=1;epoch++)for(let ackEpoch=0;ackEpoch<=1;ackEpoch++){
 const want=now>=last && issued>=now-2 && issued<=now && epoch===ackEpoch;
 if(validAck(now,issued,2,last,epoch,ackEpoch)!==want)throw Error("ack");n++;
 }
 return {projection_witness:true,frechet_four_marginals:[lo,hi],abstract_ack_cases:n,not_runtime_proof:true};
}
test();
