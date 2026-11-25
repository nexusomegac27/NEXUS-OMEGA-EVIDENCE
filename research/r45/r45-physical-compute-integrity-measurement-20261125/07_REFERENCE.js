// Pure synthetic reference, no external effects.
function envelope(l,u,e) {
 if(!l.length||l.length!==u.length||u.length!==e.length||l.some((x,i)=>![x,u[i],e[i]].every(Number.isFinite)||x<0||u[i]>1||x>u[i]||e[i]<0||e[i]>1))throw Error("invalid");
 const a=l.map((x,i)=>Math.max(0,x-e[i])),b=u.map((x,i)=>Math.min(1,x+e[i]));
 return [Math.max(0,a.reduce((x,y)=>x+y,0)-a.length+1),Math.min(...b)];
}
function test(){
 const a=envelope([.95,.95,.95,.95],[.95,.95,.95,.95],[.01,.01,.01,.01]);
 if(Math.abs(a[0]-.76)>1e-12||Math.abs(a[1]-.96)>1e-12)throw Error("envelope");
 const rates=[.5,1.5,3].map(d=>({d,tolerant_miss:[0,1].filter(r=>Math.abs(d*r)<=1).length/2}));
 if(rates[0].tolerant_miss!==1||rates[1].tolerant_miss!==.5)throw Error("Freivalds");
 let tests=0;for(let d=0;d<=4;d++)for(let x=-4;x<=4;x++)if(d>2){if([x,x+d].filter(v=>Math.abs(v)<=1).length>1)throw Error("pair");tests++}
 return {envelope:a,scalar:rates,separation_pairs:tests,independent_product:.95**4,formal_credit:false};
}
test();
