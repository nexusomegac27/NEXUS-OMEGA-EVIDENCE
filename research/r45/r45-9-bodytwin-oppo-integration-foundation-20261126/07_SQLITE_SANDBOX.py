"""Offline synthetic integration witness; not a production authorizer."""
import concurrent.futures, hashlib, json, sqlite3, tempfile, threading
from pathlib import Path

def require(ok):
    if not ok: raise RuntimeError('test failed')

def digest(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

def setup(p):
    with sqlite3.connect(p) as c:
        c.executescript('''CREATE TABLE ctl(id INTEGER PRIMARY KEY,epoch INTEGER,stopped INTEGER,budget INTEGER);
        INSERT INTO ctl VALUES(1,1,0,1);
        CREATE TABLE grants(id TEXT PRIMARY KEY,body TEXT NOT NULL,epoch INTEGER NOT NULL,expires INTEGER NOT NULL,cost INTEGER NOT NULL CHECK(cost>0));
        INSERT INTO grants VALUES('A','alpha',1,10,1),('B','beta',1,10,1);
        CREATE TABLE effects(id TEXT PRIMARY KEY,body TEXT NOT NULL,sha TEXT NOT NULL,cost INTEGER NOT NULL CHECK(cost>0));''')

def commit(p, rid, body, now, cost=1, fail=False, lost=False):
    with sqlite3.connect(p, timeout=5) as c:
        c.execute('BEGIN IMMEDIATE')
        epoch, stopped, budget=c.execute('SELECT epoch,stopped,budget FROM ctl').fetchone()
        g=c.execute('SELECT body,epoch,expires,cost FROM grants WHERE id=?',(rid,)).fetchone()
        old=c.execute('SELECT body,sha,cost FROM effects WHERE id=?',(rid,)).fetchone()
        if old: return 'DUPLICATE' if old==(body,digest(body),cost) else 'CONFLICT'
        used=c.execute('SELECT coalesce(sum(cost),0) FROM effects').fetchone()[0]
        if type(now) is not int or now<0 or type(cost) is not int or cost<=0 or not g or stopped or g[0]!=body or g[1]!=epoch or now>=g[2] or g[3]!=cost or used+cost>budget: return 'DENIED'
        c.execute('INSERT INTO effects VALUES(?,?,?,?)',(rid,body,digest(body),cost))
        if fail: raise RuntimeError('injected before commit')
    return 'UNKNOWN' if lost else 'COMMITTED'

def readback(p,rid,expected):
    with sqlite3.connect(p) as c: r=c.execute('SELECT body,sha FROM effects WHERE id=?',(rid,)).fetchone()
    return 'ABSENT' if r is None else 'VERIFIED_MOCK' if r==(expected,digest(expected)) else 'HOLD_MISMATCH'

def run():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'state.db';setup(p)
        n=100; wins=[]
        for i in range(n):
            with sqlite3.connect(p) as c:c.execute('DELETE FROM effects')
            barrier=threading.Barrier(2)
            def worker(x):
                barrier.wait();return commit(p,*x,now=1)
            with concurrent.futures.ThreadPoolExecutor(2) as e: r=list(e.map(worker,[('A','alpha'),('B','beta')]))
            require(sorted(r)==['COMMITTED','DENIED']);wins.append(r.count('COMMITTED'))
        with sqlite3.connect(p) as c:c.execute('DELETE FROM effects')
        checks={}
        checks['cost_changed']=commit(p,'A','alpha',1,2)
        checks['bool_cost']=commit(p,'A','alpha',1,True)
        checks['nan_cost']=commit(p,'A','alpha',1,float('nan'))
        checks['expiry_boundary']=commit(p,'A','alpha',10)
        checks['altered_body']=commit(p,'A','wrong',1)
        with sqlite3.connect(p) as c:c.execute('UPDATE ctl SET stopped=1')
        checks['stop']=commit(p,'A','alpha',1)
        with sqlite3.connect(p) as c:c.execute('UPDATE ctl SET stopped=0,epoch=2')
        checks['stale_epoch']=commit(p,'A','alpha',1)
        with sqlite3.connect(p) as c:c.execute('UPDATE ctl SET epoch=1') # test fixture reset only
        try: commit(p,'A','alpha',1,fail=True)
        except RuntimeError as e:require(str(e)=='injected before commit')
        checks['rollback_before_commit']=readback(p,'A','alpha')
        checks['lost_ack']=commit(p,'A','alpha',1,lost=True)
        checks['readback']=readback(p,'A','alpha')
        checks['duplicate']=commit(p,'A','alpha',1)
        checks['conflict']=commit(p,'A','other',1)
        with sqlite3.connect(p) as c:c.execute("UPDATE effects SET body='tampered' WHERE id='A'")
        checks['tampered_readback']=readback(p,'A','alpha')
        exp={k:'DENIED' for k in ['cost_changed','bool_cost','nan_cost','expiry_boundary','altered_body','stop','stale_epoch']}
        exp.update(rollback_before_commit='ABSENT',lost_ack='UNKNOWN',readback='VERIFIED_MOCK',duplicate='DUPLICATE',conflict='CONFLICT',tampered_readback='HOLD_MISMATCH')
        require(checks==exp)
        return {'sqlite_version':sqlite3.sqlite_version,'two_writer_trials':n,'exactly_one_commit':sum(wins),'budget_overruns':n-sum(wins),'checks':checks,'matched':len(checks),'formal_credit':False,'limits':'single temporary database; logical clock and trusted preloaded grant fixtures; no real crash, external effect, real signing or OS mediation; no wallclock guarantee'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
