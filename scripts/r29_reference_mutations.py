#!/usr/bin/env python3
"""Independent anti-degenerate mutation of the local reference checker only."""
import importlib.util,json,pathlib,sys
p=pathlib.Path(__file__).with_name('r29_reference_f01_f26.py')
spec=importlib.util.spec_from_file_location('r29ref',p)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
original=r.permitted
base=r.run()
r.permitted=lambda _: False
all_deny=r.run()
r.permitted=lambda _: True
all_accept=r.run()
r.permitted=original
res={
 "object":"NEXUS_OMEGA_R29R1_AXIOM_REFERENCE_MUTATION_SENSITIVITY_20261112_R0",
 "baseline":{"primary_pass":base['pass_count'],"positive_pass":base['positive_twin_pass']},
 "always_deny":{"primary_pass":all_deny['pass_count'],"positive_pass":all_deny['positive_twin_pass']},
 "always_accept":{"primary_pass":all_accept['pass_count'],"positive_pass":all_accept['positive_twin_pass']},
 "expected":{"baseline_primary":26,"baseline_positive":25,"always_deny_positive":0,"always_accept_primary":1},
 "target_sandbox":"NOT_EXECUTED",
 "device":"NOT_EXECUTED"
}
print(json.dumps(res,indent=2))
ok=base['pass_count']==26 and base['positive_twin_pass']==25 and all_deny['positive_twin_pass']==0 and all_accept['pass_count']==1
sys.exit(0 if ok else 1)
