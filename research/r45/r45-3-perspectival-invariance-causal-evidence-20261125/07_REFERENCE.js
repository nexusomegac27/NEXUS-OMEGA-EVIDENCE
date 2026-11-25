// pure algebraic diagnostics, no authority, I/O or actual device
function test(){
 const nis=(x,s)=>x.reduce((a,v,i)=>a+v*v/s[i],0);
 const e=[2,1],s=[4,1],t=[10,.1],ep=e.map((x,i)=>x*t[i]),sp=s.map((x,i)=>x*t[i]**2);
 const r={nis:nis(e,s),transformed:nis(ep,sp),wrong:nis(ep,s)};
 if(Math.abs(r.nis-r.transformed)>1e-12||Math.abs(r.wrong-r.nis)<1)throw Error("nis");
 const near=(a,b)=>Math.abs(a-b)<=1;
 const tolerance=[near(0,.75),near(.75,1.5),near(0,1.5)];
 if(tolerance.join()!=="true,true,false")throw Error("tolerance");
 const deps={A:[],B:["A"],C:["A"],D:["B","C"]};
 function valid(order){return order.length===4&&new Set(order).size===4&&order.every((x,i)=>deps[x]&&deps[x].every(p=>order.indexOf(p)>=0&&order.indexOf(p)<i))}
 const orders=[["A","B","C","D"],["A","C","B","D"],["B","A","C","D"]];
 const validity=orders.map(valid);if(validity.join()!=="true,true,false")throw Error("dag");
 const p=.2,ind=3*p*p*(1-p)+p**3;
 const raw1='{"a":1,"b":2}',raw2='{"b":2,"a":1}';
 // ASCII toy serialization only; NOT a JCS implementation.
 const toy=s=>JSON.stringify(Object.fromEntries(Object.entries(JSON.parse(s)).sort(([a],[b])=>a<b?-1:a>b?1:0)));
 return {r,tolerance,orders,validity,majority_independent:ind,majority_correlated:p,raw_strings_different:raw1!==raw2,toy_canonical_equal:toy(raw1)===toy(raw2),formal_credit:false};
}
test();
