import itertools as it, collections as co, math, json, hashlib, time, sys

def row(mask):
    a=[[mask>>(4*i+j)&1 for j in range(4)] for i in range(4)]
    r=tuple(map(sum,a)); c=tuple(map(sum,zip(*a)))
    d=tuple(sum(a[i][j] for i in range(4) for j in range(4) if i+j==k) for k in range(7))
    e=tuple(sum(a[i][j] for i in range(4) for j in range(4) if i-j==k) for k in range(-3,4))
    t=sum(a[i][j] for i in (1,2) for j in (1,2))
    return r+c,d,e,t,a[1][1],mask

def summary(groups):
    return dict(fibers=len(groups),singleton_states=sum(len(v) for v in groups.values() if len(v)==1),target_identified_states=sum(len(v) for v in groups.values() if max(v)==min(v)),max_target_width=max(max(v)-min(v) for v in groups.values()),largest_fiber=max(map(len,groups.values())))

def run():
    groups=[co.defaultdict(list) for _ in range(3)]; selected=[]
    for m in range(65536):
        b,d,e,t,p,_=row(m)
        for g,key in zip(groups,(b,b+d,b+d+e)):g[key].append(t)
        if b==(2,)*8:selected.append((d,e,t,p,m))
    s=[summary(g) for g in groups]
    def widths(idx,err):
        def dist(a,b):return max(abs(x-y) for x,y in zip(a,b)) if isinstance(a,tuple) else abs(a-b)
        w=[]
        for x in selected:
            f=[y[2] for y in selected if dist(x[idx],y[idx])<=err]
            w.append(max(f)-min(f))
        return dict(max=max(w),mean=sum(w)/len(w),identified=sum(v==0 for v in w))
    views={name:{'exact':widths(i,0),'bounded_1':widths(i,1)} for name,i in [('sum_diag',0),('diff_diag',1),('central_pixel',3),('target_sum',2)]}
    parity=[[(i,j,k) for i,j,k in it.product(range(2),repeat=3) if (i+j+k)%2==p] for p in (0,1)]
    def rays(x,axis):return sorted(tuple(v[i] for i in range(3) if i!=axis) for v in x)
    out=dict(states=65536,levels=s,selected_count=len(selected),selected_target_range=[min(x[2] for x in selected),max(x[2] for x in selected)],views=views,parity={'sets':parity,'equal_three_xrays':all(rays(parity[0],a)==rays(parity[1],a) for a in range(3))},pairwise_independent={'q_t0':[.52,.36,.12,0],'q_t04':[.48,.48,0,.04],'majority':[.12,.04],'iid':.104},geometry=[{'deg':a,'rho':rho,'var_x2':(1+math.cos(math.radians(a))**2-2*rho*math.cos(math.radians(a)))/math.sin(math.radians(a))**2} for a in (1,5,15,45,90) for rho in (0,.9)],duplicate_variance=[(1+r)/2 for r in (0,.5,.9,.99)])
    if not (s[0]['target_identified_states']<=s[1]['target_identified_states']<=s[2]['target_identified_states'] and all(v['exact']['max']<=v['bounded_1']['max'] for v in views.values()) and out['parity']['equal_three_xrays']):raise RuntimeError('invariant')
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2,allow_nan=False))
