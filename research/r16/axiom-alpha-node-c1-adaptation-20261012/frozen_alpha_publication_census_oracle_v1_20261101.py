import copy, hashlib, json
CHAIN = [
 ('245','f17196d26faa03650709601f8fecea6c50cc657d','ca8b2f9d7a5cf7371611690c2c4a52e5904f1e67',6547058731,3),
 ('247','ca8b2f9d7a5cf7371611690c2c4a52e5904f1e67','6363cd0ac7979bc4adea6407ca950baf1cbb3cd3',6547281868,3),
 ('248','6363cd0ac7979bc4adea6407ca950baf1cbb3cd3','8036ffdb2985c688705f2d29f594b8dd757a5f55',6548115987,3),
 ('249','8036ffdb2985c688705f2d29f594b8dd757a5f55','cfad6f9ad1f51efc2114249f14228aaa3a1c4cbd',6548805508,3),
 ('250','cfad6f9ad1f51efc2114249f14228aaa3a1c4cbd','8bb1861d8d548a3bec172ae892b4cda0e20ee559',6549272854,3),
 ('251','8bb1861d8d548a3bec172ae892b4cda0e20ee559','ec887632a4f1659a29c01f4db8bbf1cc79c30ae6',6549786500,3),
 ('252','ec887632a4f1659a29c01f4db8bbf1cc79c30ae6','daffb9c7f80eb3f5d12af48e66dd5306d11cec1e',6550946364,2),
]
base=[dict(pr=pr,parent=parent,main=main,receipt_id=receipt,files=[{'sha_match':True,'blob_match':True,'bytes_match':True} for _ in range(count)],checks=['success']*8,additive=True,signature=True) for pr,parent,main,receipt,count in CHAIN]
def check(records):
 if len(records)!=7:return False
 if [r['pr'] for r in records]!=[x[0] for x in CHAIN]:return False
 if records[-1]['main']!='daffb9c7f80eb3f5d12af48e66dd5306d11cec1e':return False
 for i,r in enumerate(records):
  if r['parent']!=CHAIN[i][1] or r['main']!=CHAIN[i][2]:return False
  if i and r['parent']!=records[i-1]['main']:return False
  if r['receipt_id']!=CHAIN[i][3] or len(r['files'])!=CHAIN[i][4]:return False
  if not r['additive'] or not r['signature']:return False
  if any(not all(f.values()) for f in r['files']):return False
  if len(r['checks'])!=8 or any(c!='success' for c in r['checks']):return False
 return True
cases={'positive':base}
for key,mutate in [
 ('bad_sha',lambda d:d[2]['files'][0].update(sha_match=False)),
 ('missing_receipt',lambda d:d[3].update(receipt_id=None)),
 ('failed_ci',lambda d:d[4]['checks'].__setitem__(7,'failure')),
 ('broken_parent',lambda d:d[5].update(parent='0'*40)),
 ('historical_rewrite',lambda d:d[6].update(additive=False)),
]:
 d=copy.deepcopy(base);mutate(d);cases[key]=d
out={k:check(v) for k,v in cases.items()}
print(json.dumps({'oracle_cases':out,'passed':sum(v==(k=='positive') for k,v in out.items()),'total':len(out),'scope':'STRUCTURAL_AUDIT_FIXTURE_ONLY_NO_API_ACCESS','positive_denominator':len(base),'file_denominator':sum(len(x['files']) for x in base),'ci_denominator':sum(len(x['checks']) for x in base)},sort_keys=True))
assert out['positive'] and all(not v for k,v in out.items() if k!='positive')
