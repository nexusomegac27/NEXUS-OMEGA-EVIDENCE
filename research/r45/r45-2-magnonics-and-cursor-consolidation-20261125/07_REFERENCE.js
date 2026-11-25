// New pure synthetic diagnostics: no hardware model, no runtime authority.
function test(){
 const rho=.8, rows=[5,10].map(n=>{let f=1;for(let k=1;k<n;k++)f+=2*(n-k)/n*rho**k;return {n,f,var_mean:f/n}});
 const factorizations=[[1,2,3],[2,1,3],[3,2,1]].map(a=>({parts:a,composite:a.reduce((x,y)=>x*y,1)}));
 if(!factorizations.every(x=>x.composite===6))throw Error("factorization");
 let n=0,flips=0,outside=0;for(let i=-20;i<=20;i++)for(let j=-5;j<=5;j++){const x=i/10,e=j/10,y=x+e,flip=(x>=0)!==(y>=0);n++;if(flip){flips++;if(Math.abs(x)>.5+1e-12)outside++}}
 if(outside)throw Error("threshold bound");
 return {ar1:rows,factorizations,threshold_cases:n,threshold_flips:flips,flips_outside_bound:outside,delta:.5,formal_credit:false};
}
test();
