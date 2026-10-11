#!/usr/bin/env python3
"""R26/P26 scoped spectral re-execution; deterministic synthetic C1, NOT NF05/NF06."""
import numpy as np
CASES=((32,2,7),(32,4,7),(32,8,5),(32,16,5),(64,2,11),(64,4,9),(64,8,7),(64,16,7))
EXPECT_MAX=(1.5421710622,1.9906732197,1.0377893000,1.3453631021,2.8398242536,2.2599911942,1.5307947692,1.9895641537)
EXPECT_SUM=(.8673973466,1.3757786573,.9792479015,1.3453631021,.9213796550,.9466404753,.8452313734,1.3504012609)
def dominant_nonradial(J):
    eig=np.linalg.eigvals(J); i=np.argmin(abs(eig-1))
    assert abs(eig[i]-1)<1e-9
    return float(np.max(abs(np.delete(eig,i))))
def run(N,k,L):
    th=2*np.pi*np.arange(N)/N
    W=((1+np.cos(th[:,None]-th[None,:]))/2)**k
    A=np.array([(i-L//2)%N for i in range(L)])
    WA=W[np.ix_(A,A)]
    v=np.linalg.solve(np.eye(L)-WA,np.ones(L))
    gm=-1/v[L//2];gs=-1/v.sum()
    r=np.zeros(N);r[A]=-gm*v
    s=np.zeros(N);s[A]=-gs*v
    assert (r[A]>0).all() and (s[A]>0).all()
    assert abs(np.maximum(W@r-gm*r.max(),0)-r).max()<1e-10
    assert abs(np.maximum(W@s-gs*s.sum(),0)-s).max()<1e-10
    Jm=WA-gm*np.outer(np.ones(L),np.eye(L)[L//2])
    Js=WA-gs*np.ones((L,L))
    B=np.zeros((L,L//2))
    for d in range(1,L//2+1):
        B[L//2-d,d-1]=1/np.sqrt(2)
        B[L//2+d,d-1]=-1/np.sqrt(2)
    assert abs(B.T@Jm@B-B.T@Js@B).max()<1e-12
    return dominant_nonradial(Jm),dominant_nonradial(Js)
if __name__=="__main__":
    rows=[run(*q) for q in CASES]
    for i,(m,s) in enumerate(rows):
        assert abs(m-EXPECT_MAX[i])<1e-8,(i,m)
        assert abs(s-EXPECT_SUM[i])<1e-8,(i,s)
    assert sum(m>1+1e-8 for m,_ in rows)==8
    assert sum(s>1+1e-8 for _,s in rows)==3
    print("PASS_SCOPED_SYNTHETIC_REPRO / MAX 8/8, SUM 3/8 / C1_DESCRIPTIVE_ONLY")
