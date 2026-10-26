#!/usr/bin/env python3
"""Read-only, fail-closed static collision audit for a restricted unittest fixture idiom.

Research-only. It does not execute the supplied oracle or approve candidate tests.
"""
import ast
import hashlib
import json
import sys
from pathlib import Path

class Unsupported(Exception):
    pass

def is_name(node, value):
    return isinstance(node, ast.Name) and node.id == value

def record_defaults(tree):
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'record']
    if len(functions) != 1:
        raise Unsupported('record function absent or ambiguous')
    fn = functions[0]
    if len(fn.args.args) != 1 or fn.args.args[0].arg != 'id' or fn.args.kwarg is None or fn.args.kwarg.arg != 'kwargs':
        raise Unsupported('record signature differs')
    if len(fn.body) != 3:
        raise Unsupported('record body differs')
    assign, update, ret = fn.body
    if not (isinstance(assign, ast.Assign) and len(assign.targets) == 1 and is_name(assign.targets[0], 'r')):
        raise Unsupported('record defaults not literal assignment')
    if not (isinstance(update, ast.Expr) and isinstance(update.value, ast.Call) and isinstance(update.value.func, ast.Attribute) and is_name(update.value.func.value,'r') and update.value.func.attr == 'update' and len(update.value.args)==1 and is_name(update.value.args[0], 'kwargs') and not update.value.keywords):
        raise Unsupported('record update not recognized')
    if not (isinstance(ret, ast.Return) and is_name(ret.value, 'r')):
        raise Unsupported('record return differs')
    if not isinstance(assign.value, ast.Dict):
        raise Unsupported('record defaults must be dict')
    defaults = {}
    for key, val in zip(assign.value.keys, assign.value.values):
        k = ast.literal_eval(key)
        if not isinstance(k, str) or k in defaults:
            raise Unsupported('invalid default key')
        if k == 'id' and is_name(val, 'id'):
            defaults[k] = None
        else:
            defaults[k] = ast.literal_eval(val)
    if 'id' not in defaults:
        raise Unsupported('record id default missing')
    return defaults

def value(node, defaults):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, (ast.List, ast.Tuple)):
        return [value(x,defaults) for x in node.elts]
    if isinstance(node, ast.Dict):
        keys=[value(k,defaults) for k in node.keys]
        if not all(isinstance(k,str) for k in keys) or len(keys)!=len(set(keys)):
            raise Unsupported('duplicate or nonstring keys')
        return {k:value(v,defaults) for k,v in zip(keys,node.values)}
    if isinstance(node, ast.Call) and is_name(node.func, 'record'):
        if len(node.args)!=1 or not node.keywords or any(k.arg is None for k in node.keywords):
            # No kwargs is also valid; the guard below is intentionally separate.
            if len(node.args)!=1 or any(k.arg is None for k in node.keywords):
                raise Unsupported('unsupported record invocation')
        out=dict(defaults)
        out['id']=value(node.args[0],defaults)
        keys=[k.arg for k in node.keywords]
        if len(keys)!=len(set(keys)) or 'id' in keys:
            raise Unsupported('duplicate record keyword')
        out.update({k.arg:value(k.value,defaults) for k in node.keywords})
        return out
    raise Unsupported('unsupported expression')

def test_calls(fn):
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and is_name(n.func,'output') and len(n.args)==1 and not n.keywords:
            yield n.args[0], 'ZERO'
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ('assertNotEqual','assertEqual') and len(n.args)==2:
            left,right=n.args
            if isinstance(left,ast.Attribute) and left.attr=='returncode' and isinstance(left.value,ast.Call) and is_name(left.value.func,'run') and len(left.value.args)==1 and isinstance(right,ast.Constant) and right.value==0:
                yield left.value.args[0], ('NONZERO' if n.func.attr=='assertNotEqual' else 'ZERO')

def audit(source):
    tree=ast.parse(source)
    defaults=record_defaults(tree)
    groups={}
    unsupported=[]
    total=0
    for cls in tree.body:
        if not isinstance(cls,ast.ClassDef):
            continue
        for fn in cls.body:
            if not isinstance(fn,ast.FunctionDef) or not fn.name.startswith('test_'):
                continue
            for arg,expect in test_calls(fn):
                try:
                    payload=value(arg,defaults)
                    raw=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
                except (Unsupported,ValueError,TypeError) as exc:
                    unsupported.append({'test':fn.name,'reason':str(exc)})
                    continue
                total+=1
                digest=hashlib.sha256(raw).hexdigest()
                groups.setdefault(digest,[]).append({'test':fn.name,'expect':expect,'bytes':len(raw)})
    conflicts=[{'sha256':key,'cases':items} for key,items in sorted(groups.items()) if len({x['expect'] for x in items})>1]
    status='CONFLICT' if conflicts else ('INCOMPLETE' if unsupported or total==0 else 'NO_CONFLICT_IN_SUPPORTED_CASES')
    return {'status':status,'supported_cases':total,'unsupported_cases':unsupported,'conflicts':conflicts,'source_execution':'NOT_PERFORMED','claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def main(argv):
    if len(argv)!=2:
        raise SystemExit('usage: audit.py FROZEN_ORACLE.py')
    try:
        src=Path(argv[1]).read_text(encoding='utf-8')
        result=audit(src)
    except (OSError,UnicodeError,SyntaxError,Unsupported) as exc:
        print(json.dumps({'status':'SOURCE_UNSUPPORTED','reason':str(exc),'source_execution':'NOT_PERFORMED'}))
        return 2
    print(json.dumps(result,sort_keys=True,ensure_ascii=False))
    return 1 if result['status']!='NO_CONFLICT_IN_SUPPORTED_CASES' else 0

if __name__=='__main__':
    sys.exit(main(sys.argv))
