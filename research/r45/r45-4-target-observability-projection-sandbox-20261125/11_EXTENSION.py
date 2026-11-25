# Repackaged exploratory extension (import path adapted for GitHub).
import importlib.util,json
spec=importlib.util.spec_from_file_location("sandbox","08_SANDBOX.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
S=[(d,e,t,p,m) for m in range(65536) for b,d,e,t,p,_ in [mod.row(m)] if b==(2,)*8]
def dist(a,b):return max(abs(x-y) for x,y in zip(a,b)) if isinstance(a,tuple) else abs(a-b)
out={}
for name,i in [('sum_diag',0),('diff_diag',1),('central_pixel',3),('target_sum',2)]:
    w,x,y=max(((abs(x[2]-y[2]),x,y) for x in S for y in S if dist(x[i],y[i])<=2),key=lambda v:v[0])
    out[name]={'worst_width_all_admissible_observations':w,'witness_masks':[x[4],y[4]],'targets':[x[2],y[2]],'view_values':[x[i],y[i]]}
print(json.dumps(out,indent=2))
