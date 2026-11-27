// R46-5 independent analytic and seeded Monte Carlo witnesses, not a UKF implementation.
function run(){
 let seed=46505;const U=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return(seed+.5)/4294967296},Z=()=>Math.sqrt(-2*Math.log(U()))*Math.cos(2*Math.PI*U());
 const n=100,N=30000,b=.25,r=.04,R=r+b,vc=b+r/n,vw=R/n,Pc=vc/(1+vc),Pw=vw/(1+vw),Kc=1/(1+vc),Kw=1/(1+vw);
 const trueErrWrong=(1-Kw)**2+Kw**2*vc,expectedWrong=trueErrWrong/Pw;
 const c=-2*Math.log(.05),gmean=2-c*.05/.95;
 let neC=0,neW=0,errC=0,errW=0,coverC=0,coverW=0,raw=0,accepted=0,post=0,alt=0,alt2=0,raw2=0,lag=0;
 for(let i=0;i<N;i++){const x=Z(),bias=Math.sqrt(b)*Z(),y=x+bias+Math.sqrt(r/n)*Z(),ec=x-Kc*y,ew=x-Kw*y;errC+=ec*ec;errW+=ew*ew;neC+=ec*ec/Pc;neW+=ew*ew/Pw;coverC+=Math.abs(ec)<=1.95996398454*Math.sqrt(Pc)?1:0;coverW+=Math.abs(ew)<=1.95996398454*Math.sqrt(Pw)?1:0;
 const a=Z()**2,d=Z()**2,v=a+d,w=.1*a+1.9*d;raw+=v;raw2+=v*v;alt+=w;alt2+=w*w;if(v<=c){accepted++;post+=v}const z1=bias+Math.sqrt(r)*Z(),z2=bias+Math.sqrt(r)*Z();lag+=z1*z2/R;}
 const s=.009171949489023268,t=.30044844215811695,vr=(t/s)**2;
 const res={shared_bias:{n,trials:N,P_correct:Pc,P_naive:Pw,expected_naive_NEES:expectedWrong,observed_NEES_correct:neC/N,observed_NEES_naive:neW/N,rmse_correct:Math.sqrt(errC/N),rmse_naive:Math.sqrt(errW/N),coverage95_correct:coverC/N,coverage95_naive:coverW/N,correlation_expected:b/R,correlation_moment_observed:lag/N},gating:{threshold:c,expected_raw:2,expected_accepted:gmean,observed_raw:raw/N,observed_accepted:post/accepted,acceptance:accepted/N},mean_equal:{expected_mean_both:2,expected_variance_nominal:4,expected_variance_misspecified:2*(.1**2+1.9**2),observed_mean_nominal:raw/N,observed_mean_misspecified:alt/N,observed_variance_nominal:raw2/N-(raw/N)**2,observed_variance_misspecified:alt2/N-(alt/N)**2},r21_conditional:{transverse_variance_ratio:vr,expected_3d_NIS_if_P0_and_zero_z_variance:2*vr,normalized_mean_if_P0:2*vr/3,transverse_ratio_with_equal_predictive_var_1:(1+t*t)/(1+s*s)},limits:"Shared scalar bias modeled independent of x; mean of n Gaussian samples drawn directly, not n-step recursive filter. Exact Gaussian posterior and linear comparator, not UKF; iid trajectories; chi2_2 gating only; no actual OPPO raw/physical calibration."};
 const checks={correct_nees:Math.abs(neC/N-1)<.04,naive_nees:Math.abs(neW/N/expectedWrong-1)<.04,correct_coverage:Math.abs(coverC/N-.95)<.015,wrong_coverage:coverW/N<.3,gated_mean:Math.abs(post/accepted-gmean)<.04,gating_contracts:gmean<2,equal_mean:Math.abs(raw/N-alt/N)<.05,variance_distinct:res.mean_equal.observed_variance_misspecified>res.mean_equal.observed_variance_nominal*1.5,ratio:vr>1000&&res.r21_conditional.transverse_ratio_with_equal_predictive_var_1<1.1};
 if(!Object.values(checks).every(Boolean))throw Error(JSON.stringify({checks,res}));return {checks,...res};
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
