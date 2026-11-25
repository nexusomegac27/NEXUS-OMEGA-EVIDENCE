"""AXIOM synthetic reference controls; no system actions."""
from itertools import product
from math import prod

def coverage(rows):
    if not rows or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError('nonrectangular/empty')
    if any(type(x) is not bool for r in rows for x in r):
        raise ValueError('boolean outcomes required')
    p = [sum(r[i] for r in rows)/len(rows) for i in range(len(rows[0]))]
    return p, sum(all(r) for r in rows)/len(rows), prod(p)

def dispatch(acks, registered, scope, lease, fresh, stop, external_gate):
    return bool(acks and registered and scope and lease and fresh and not stop and external_gate)

if __name__ == '__main__':
    for r in ([[True,True],[False,False]], [[True,False],[False,True]]):
        print('coverage', coverage(r))
    cases = list(product([False, True], repeat=7))
    permitted = [c for c in cases if dispatch(*c)]
    if permitted != [(True,True,True,True,True,False,True)]:
        raise RuntimeError('gate invariant')
    print('group gate reference',len(cases),'states',len(permitted),'permit')
    print('NOT a runtime or corrigibility proof')
