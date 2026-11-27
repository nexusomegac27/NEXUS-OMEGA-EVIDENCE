// Synthetic summary-identifiability witnesses, no raw OPPO measurements.
function run(){
 const mean=x=>x.reduce((s,v)=>s+v,0)/x.length;
 const sd=x=>Math.sqrt(mean(x.map(v=>(v-mean(x))**2)));
 const lag=x=>{let m=mean(x);return mean(x.slice(1).map((v,i)=>(v-m)*(x[i]-m))) / mean(x.map(v=>(v-m)**2))};
 const a=[1,-1,1,-1,1,-1,1,-1],b=[1,1,1,1,-1,-1,-1,-1];
 const t=a.map((_,i)=>i/100);
 const summary=x=>({n:x.length,mean:mean(x),population_sd:sd(x),rate:(x.length-1)/(t.at(-1)-t[0])});
 const one=summary(a),two=summary(b);
 const norm=v=>Math.hypot(...v);
 const v1=[[0,0,10],[0,0,10]],v2=[[10,0,0],[10,0,0]];
 // Same static output 10 under two different affine calibration models, assuming nominal input 10.
 const models=[{scale:1,bias:0},{scale:.9,bias:1}].map(m=>({...m,output_at_10:m.scale*10+m.bias,output_at_minus10:m.scale*(-10)+m.bias}));
 const g=9.80665,delta=.1,values=[g-delta,g+delta];
 const ar={abs_mean_residual:Math.abs(mean(values)-g),mean_abs_residual:mean(values.map(x=>Math.abs(x-g)))};
 const rates={acc:(7014-1)/70.022492373,gyro:(7004-1)/69.922634925,median_reciprocal:1/.009984687,mean_minus_conventional_g:9.832738001091458-g};
 const checks={aggregate_same:JSON.stringify(one)===JSON.stringify(two),different_lag:lag(a)!==lag(b),same_norm_different_vector:v1.map(norm).join()===v2.map(norm).join()&&JSON.stringify(v1)!==JSON.stringify(v2),one_pose_scale_bias_ambiguous:models[0].output_at_10===models[1].output_at_10&&models[0].output_at_minus10!==models[1].output_at_minus10,mean_abs_not_abs_mean:ar.mean_abs_residual>ar.abs_mean_residual,acc_rate_match:Math.abs(rates.acc-100.15353299112422)<1e-12,gyro_rate_match:Math.abs(rates.gyro-100.15354838260195)<1e-12};
 if(!Object.values(checks).every(Boolean))throw Error("witness failed");
 return {checks,synthetic:{one,two,lag_product_normalized_A:lag(a),lag_product_normalized_B:lag(b),v1,v2,models,ar},aggregate_arithmetic:rates,limits:"Synthetic scalar ordering and ACC-only vector witnesses; no joint physically realized trajectory, no raw replay, population SD for toy only; reported raw ddof unknown. No formal or physical gate credit."};
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
