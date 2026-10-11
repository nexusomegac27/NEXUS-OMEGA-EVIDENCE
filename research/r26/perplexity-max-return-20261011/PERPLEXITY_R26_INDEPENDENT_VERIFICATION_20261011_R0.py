#!/usr/bin/env python3
"""NEXUS OMEGA R26 - Perplexity independent verification of the MISTRAL/VIBE MAX return (C1, exploratory).
Model: N ring units, W_ij=((1+cos(th_i-th_j))/2)^k, discrete map r <- relu(W r - g*P(r)),
P=max (MODEL_MAX) or sum (MODEL_SUM); zero input, zero noise. Research only; no NF-05/NF-06 trials.
Checks: (1) AXIOM point reproduction, (2) eigenvalue sign/realness and time-discretisation robustness,
(3) parity of unstable mode, (4) parameter sweep, (5) two-peak replay under three declared injection shapes.
"""
import numpy as np, platform
print("python", platform.python_version(), "numpy", np.__version__)
def Wmat(N,k):
    th=2*np.pi*np.arange(N)/N; return ((1+np.cos(th[:,None]-th[None,:]))/2)**k
def arc(N,L): return np.array([(i-(L//2))%N for i in range(L)])
def point(N,k,L,arm):
    W=Wmat(N,k); A=arc(N,L); WA=W[np.ix_(A,A)]; c=L//2
    v=np.linalg.solve(np.eye(L)-WA,np.ones(L)); g=-1/v[c] if arm=="MAX" else -1/v.sum()
    r=np.zeros(N); r[A]=-g*v
    if g<=0 or (r[A]<=0).any(): return None
    drive=W@r-g*(r.max() if arm=="MAX" else r.sum()); inact=np.setdiff1d(np.arange(N),A)
    J=WA-g*(np.outer(np.ones(L),np.eye(L)[c]) if arm=="MAX" else np.ones((L,L)))
    ev,V=np.linalg.eig(J); i=np.argmin(abs(ev-1)); idx=[j for j in range(L) if j!=i]
    j=max(idx,key=lambda j:abs(ev[j])); x=V[:,j].real
    par="odd" if np.allclose(x,-x[::-1],atol=1e-8) else ("even" if np.allclose(x,x[::-1],atol=1e-8) else "mixed")
    srt=np.sort(r[A]); return dict(W=W,A=A,v=v,g=g,r=r,res=np.abs(np.maximum(drive,0)-r).max(),
        margin=-drive[inact].max(), peak_gap=srt[-1]-srt[-2], radial=ev[i], lam=ev[j], parity=par)
print("\n[1] AXIOM point N=32 k=8 L=5")
P={}
for arm in ["MAX","SUM"]:
    d=point(32,8,5,arm); P[arm]=d
    print(f"{arm}: g={d['g']:.12f} residual={d['res']:.2e} inactive_margin={d['margin']:.6f} peak_gap={d['peak_gap']:.6f} "
          f"radial={d['radial'].real:.12f} lam_nonradial={d['lam'].real:.10f}{'+%.1ei'%d['lam'].imag if d['lam'].imag else ''} parity={d['parity']}")
assert np.isclose(P["MAX"]["g"],1.9807280461434622,atol=1e-10) and np.isclose(P["SUM"]["g"],0.6050068144805235,atol=1e-10)
assert np.isclose(abs(P["MAX"]["lam"]),1.0377893000491,atol=1e-9) and np.isclose(abs(P["SUM"]["lam"]),0.9792479,atol=1e-6)
print("\n[2] Time discretisation: Euler r += dt(-r+F(r)) -> mu = 1+dt(lam-1); continuous: Re(lam)-1")
for arm in ["MAX","SUM"]:
    lam=P[arm]["lam"]; assert abs(lam.imag)<1e-12
    print(arm, "real eigenvalue:", True, "| continuous Re(lam)-1 = %+.6f"%(lam.real-1),
          "| " + " ".join("dt=%g:|mu|=%.6f"%(dt,abs(1+dt*(lam-1))) for dt in [1,0.5,0.1,0.01]))
print("\n[3]+[4] Sweep N in {32,64}, k in {2,4,8,16}, contiguous odd arcs L=3..15 (consistent & strict inactive margin only)")
cnt={"MAX":[0,0],"SUM":[0,0]}
for N in [32,64]:
  for k in [2,4,8,16]:
    for L in range(3,16,2):
      for arm in ["MAX","SUM"]:
        d=point(N,k,L,arm)
        if d is None or d["margin"]<=1e-9 or d["res"]>1e-10: continue
        unst=abs(d["lam"])>1+1e-9; cnt[arm][0]+=1; cnt[arm][1]+=unst
        print(f"N={N} k={k:2d} L={L:2d} {arm} g={d['g']:.5f} lam={d['lam'].real:.5f} parity={d['parity']} -> {'UNSTABLE' if unst else 'shape-stable'}")
print("summary unstable/consistent:", {a:f"{c[1]}/{c[0]}" for a,c in cnt.items()})
print("\n[5] Two-peak replay N=32 k=8, own g per arm, 3000 steps; amplitude renormalised per step for measurement only (exact by homogeneity)")
d=P["MAX"]; W,A,N=d["W"],d["A"],32
def npeaks(r,thr=0.5):
    m=r.max(); return sum(1 for i in range(N) if r[i]>=thr*m and r[i]>r[i-1] and r[i]>=r[(i+1)%N])
def run(arm,g,r,T=3000):
    lm=0.0
    for t in range(T):
        r=np.maximum(W@r-g*(r.max() if arm=="MAX" else r.sum()),0); m=r.max()
        if m==0: return f"COLLAPSE(step {t})"
        lm+=np.log(m); r=r/m
    p=npeaks(r); return ("WTA_ONE_BUMP" if p==1 else f"PERSISTENT_MULTI({p})")+f" mean_log_amp/step={lm/T:+.4f}"
shapes={"delta":lambda c,a,arm: a*np.eye(N)[c],
        "fixedpoint_shape":lambda c,a,arm: a*np.roll(P[arm]["r"]/P[arm]["r"].max(),c),
        "gauss_sigma2":lambda c,a,arm: a*np.exp(-0.5*(((np.arange(N)-c+N/2)%N-N/2)/2)**2)}
for arm in ["MAX","SUM"]:
    g=P[arm]["g"]; base=P[arm]["r"]/P[arm]["r"].max()
    print(f"{arm} single exact bump: {run(arm,g,base.copy())} | +1e-6 at centre: {run(arm,g,base+1e-6*np.eye(N)[0])}")
    for nm,f in shapes.items():
        for b in [1.0,0.8,0.5]:
            for sep in [16,8]:
                print(f"  {arm} {nm:16s} 1.0/{b} sep={sep:2d}: {run(arm,g,f(0,1.0,arm)+f(sep,b,arm))}")
print("\nLIMIT: MISTRAL/VIBE producer injection shape unknown; outcome classes depend on it (see [5]).")
