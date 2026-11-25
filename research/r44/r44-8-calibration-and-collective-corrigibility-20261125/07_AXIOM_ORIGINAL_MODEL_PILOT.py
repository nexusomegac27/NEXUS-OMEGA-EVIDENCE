import hashlib,types,time,json, numpy as np, warnings
from scipy.optimize import least_squares
from scipy import __version__ as scipy_version
p='/tmp/nexus_model5.py'; source=open(p,'rb').read(); expect='9c34bfec2709de8a5c7f45d03c4cf880e2dac8afb6fc7a75f1b64004aa3217c2'
if hashlib.sha256(source).hexdigest()!=expect: raise RuntimeError('source')
# fixed diagnostic design: paired, 64 trials per span, known AR1 rho=.8, same source init true, no postselection; strict coverage requires finite positive interval and success; no full original replay.
N=64; seed=8448001; rng=np.random.default_rng(seed); draws=rng.standard_normal((N,5)); orig=types.ModuleType('orig'); fix=types.ModuleType('fix'); exec(compile(source,p,'exec'),orig.__dict__); old=b'return Lc @ (y - f_nl(theta, t))'; new=b'return Lc.T @ (y - f_nl(theta, t))';
if source.count(old)!=1:raise RuntimeError('delta')
patched=source.replace(old,new);exec(compile(patched,'candidate','exec'),fix.__dict__)
S=orig.ar1(.8,5);W=np.linalg.inv(S); E=draws@np.linalg.cholesky(S).T;theta=orig.THETA_TRUE; rows=[]; t0=time.monotonic()
for span in (.8,4.):
 t=np.linspace(.1,.1+span,5)
 y0=orig.f_nl(theta,t)
 for label,m in [('OLD',orig),('COR',fix)]:
  hits=[];succ=0;valid=0;obj=[]; grad=[]; errors=[]; failures=0
  for e in E:
   with warnings.catch_warnings():
    warnings.simplefilter('ignore');
    try:
     est,it,ok=m.gls_nonlinear(y0+e,t,W,theta); s=bool(ok and np.isfinite(est).all()); succ+=s
     hw=m.ci_nonlinear(est,t,W);good=bool(s and np.isfinite(hw).all() and (hw>0).all());valid+=good;hits.append((np.abs(est-theta)<=hw) if good else np.zeros(4,bool));
     if s:
      r=y0+e-m.f_nl(est,t); obj.append(float(r@W@r));errors.append((est-theta).tolist())
    except (ValueError, np.linalg.LinAlgError, FloatingPointError, OverflowError):
     failures+=1;hits.append(np.zeros(4,bool))
  h=np.array(hits);rows.append(dict(span=span,arm=label,n=N,success=succ,valid_ci=valid,exceptions=failures,per_param_hits=h.sum(0).tolist(),joint_hits=int(h.all(1).sum()),mean_target_sse=float(np.mean(obj)),rmse=np.sqrt(np.mean(np.square(errors),axis=0)).tolist()))
print(json.dumps(dict(source_sha256=expect,patched_sha256=hashlib.sha256(patched).hexdigest(),n=N,seed=seed,rho=.8,init='theta_true',numpy=np.__version__,scipy=scipy_version,rows=rows,wall_s=time.monotonic()-t0),indent=2))
