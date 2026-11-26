import json, math, collections, random, statistics, hashlib
from pathlib import Path
# Finite abstraction. Two independent requests, one shared unit of budget, external deadline.
# Status P pending, S success, H timeout. Debate changes a visible bit, never spends authority.
def transitions(s,mode):
    t,spent,rs,bit=s
    if 'P' not in rs:return [('stutter',s)]
    z=[('debate',(t,spent,rs,1-bit))]
    if t<3 and mode!='no_tick':
        u=t+1; z.append(('tick',(u,spent,tuple('H' if x=='P' and u==3 else x for x in rs),bit)))
    if t<3 and spent<1:
        for i,x in enumerate(rs):
            if x=='P':
                a=list(rs);a[i]='S';z.append((f'commit_{i}',(t,spent+1,tuple(a),bit)))
    return z

def graph(mode):
    init=(0,0,('P','P'),0);q=collections.deque([init]);seen={init};edges={}
    while q:
        s=q.popleft();edges[s]=transitions(s,mode)
        for _,v in edges[s]:
            if v not in seen:seen.add(v);q.append(v)
    # Every nonterminal cycle must consist of debate edges only:
    # time and spent never decrease, number of pending requests never increases.
    # All pending states admit a debate 2-cycle; weak fairness of Next does not exclude it.
    loops=[]
    for s in sorted(seen):
        if 'P' not in s[2]:continue
        b=next(v for a,v in edges[s] if a=='debate'); assert ('debate',s) in edges[b]
        tick_continuous=all(any(a=='tick' for a,_ in edges[v]) for v in (s,b))
        loops.append((s,b,tick_continuous))
    assert all(0<=s[1]<=1 and s[1]==s[2].count('S') for s in seen)
    return {'states':len(seen),'edges':sum(map(len,edges.values())), 'nonterminal_debate_cycles':len(loops)//2,'cycles_allowed_WF_global_next':len(loops)//2,'cycles_allowed_WF_tick':sum(not x[2] for x in loops)//2,'terminal_states':sum('P' not in s[2] for s in seen),'sample_lasso':loops[0], 'deadline_reachable':any(s[0]==3 for s in seen),'all_terminal_by_3_external_ticks':all('P' not in s[2] for s in seen if s[0]==3) if any(s[0]==3 for s in seen) else None}

def budget():
    # Exhaustive schedules for two checks and two commits, each check before its commit.
    import itertools
    schedules=[]
    for order in itertools.permutations(('check_A','commit_A','check_B','commit_B')):
        if any(order.index('check_'+i)>order.index('commit_'+i) for i in 'AB'):continue
        bal=1; permission={};hist=[]
        for a in order:
            op,i=a.split('_')
            if op=='check':permission[i]=bal>=1
            elif permission[i]:bal-=1
            hist.append(bal)
        atomic=1;success=0
        for a in order:
            if a.startswith('commit') and atomic>=1:atomic-=1;success+=1
        schedules.append({'order':order,'snapshot_balance':bal,'atomic_balance':atomic,'snapshot_overrun':bal<0,'atomic_overrun':atomic<0})
    return schedules

def evidence():
    # Identical submitted graph and report, different actual causal dependency.
    worlds=[{'observed':['source->derived'],'actual':['source->derived'],'authorized':True}, {'observed':['source->derived'],'actual':['source->derived','untrusted->derived'],'authorized':False}]
    assert worlds[0]['observed']==worlds[1]['observed'] and worlds[0]['authorized']!=worlds[1]['authorized']
    # Quorum: independently validated genuine counterexample blocks, failure to refute is not proof.
    cases=[]
    for complete,attempt,reproduction,counterexample in __import__('itertools').product([False,True],repeat=4):
        verdict='REJECT_OR_HOLD' if counterexample else 'C1_REVIEW_ELIGIBLE' if complete and attempt and reproduction else 'HOLD_NO_QUORUM'
        cases.append({'complete':complete,'attempt':attempt,'reproduction':reproduction,'counterexample':counterexample,'verdict':verdict})
    return {'worlds':worlds,'quorum_cases':cases,'intermittent_enablement':{'cycle':['ready','not_ready'],'commit_taken':False,'weak_fairness_commit':True,'strong_fairness_commit':False}}

def monitor():
    # Mixture over start times 1..H; future components remain at one until their start.
    # With equal weights one can update aggregate active wealth without keeping every component.
    H=200;n=2000;p=.1;q=.3;rng=random.Random(45707);data={}
    for regime in ('null','abrupt','gradual','reported_null_paired_abrupt'):
        crosses=[];actual_cross=[]
        for j in range(n):
            draws=[rng.random() for _ in range(H)]
            def run(which):
                active=0.0
                for t,u in enumerate(draws,1):
                    rate=p if which=='null' or t<=50 else q if which=='abrupt' else p+(q-p)*(t-50)/150
                    x=u<rate;active=(active+1)*(q/p if x else (1-q)/(1-p))
                    wealth=(active+H-t)/H
                    if wealth>=20:return t
                return None
            c=run('null' if regime=='reported_null_paired_abrupt' else regime);crosses.append(c)
            if regime=='reported_null_paired_abrupt':actual_cross.append(run('abrupt'))
        def stats(vals):
            post=[t-50 for t in vals if t is not None and t>50];early=sum(t is not None and t<=50 for t in vals)
            return {'alarms':sum(t is not None for t in vals),'early':early,'post_change':len(post),'conditional_median_delay':statistics.median(post) if post else None,'no_alarm':sum(t is None for t in vals)}
        data[regime]=stats(crosses)
        if actual_cross:data[regime]['paired_actual']=stats(actual_cross)
    return data

if __name__=='__main__':
    g=graph('reference');m=graph('no_tick');b=budget();e=evidence();d=monitor()
    assert g['cycles_allowed_WF_tick']==0 and m['cycles_allowed_WF_tick']>0 and any(x['snapshot_overrun'] for x in b) and not any(x['atomic_overrun'] for x in b)
    print(json.dumps({'reference':g,'no_tick_mutant':m,'budget_schedules':b,'evidence':e,'monitor':d,'formal_credit':False},indent=2,allow_nan=False))
