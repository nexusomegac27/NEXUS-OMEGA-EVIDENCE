"""R15 independent synthetic evaluator, frozen before implementation.
Oracle: dense point sampling of a sector expanded by location uncertainty.
This does not validate a real 3D engine, GPS accuracy, or browser network behavior.
"""
import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = {
    "profile": "R15_SYNTHETIC_ENU_ONLY",
    "source_ref": "synthetic://manifest-v1",
    "source_provenance": "LOCAL_VERIFIED",
    "source_available": True,
    "crs": "LOCAL_ENU_SYNTHETIC",
    "pose": {"x_m": 0.0, "y_m": 0.0, "bearing_deg": 0.0,
             "bearing_source": "DEVICE_HEADING_VERIFIED", "bearing_uncertainty_deg": 5.0,
             "gps_accuracy_m": 10.0, "timestamp_s": 990},
    "now_s": 1000,
    "max_age_s": 30,
    "tile_size_m": 100,
    "world_bounds_m": [-800, -800, 800, 800],
    "fov_deg": 70.0,
    "range_m": 450.0,
    "max_tiles": 200,
    "allow_network": False,
    "operator_consent": True,
    "view_only": True,
    "claim_ceiling": "C1_DESCRIPTIVE_ONLY"
}

def invoke(script, payload):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'input.json'
        path.write_text(json.dumps(payload, allow_nan=False, sort_keys=True), encoding='utf-8')
        result = subprocess.run([sys.executable, str(script), str(path)], text=True, capture_output=True, timeout=12)
    try:
        doc = json.loads(result.stdout)
    except Exception:
        return None, f'exit={result.returncode}, stdout={result.stdout[:120]!r}, stderr={result.stderr[:120]!r}'
    return doc, f'exit={result.returncode}'

def check_hold(script, name, patch):
    data=copy.deepcopy(BASE)
    if callable(patch): patch(data)
    else:
        for k,v in patch.items(): data[k]=v
    got, err=invoke(script,data)
    ok = isinstance(got,dict) and got.get('state') == 'HOLD_SCOPED' and got.get('selected_tile_ids') == [] and got.get('eligible_for_authoritative_claim') is False
    return name,ok,err+(f' {got}' if not ok else '')

def check_ready(script,name,patch=None):
    data=copy.deepcopy(BASE)
    if patch: patch(data)
    got,err=invoke(script,data)
    ok=(isinstance(got,dict) and got.get('state')=='READY_P0_SYNTHETIC' and isinstance(got.get('selected_tile_ids'),list)
        and got.get('eligible_for_authoritative_claim') is False and got.get('network_requests')==0
        and got['selected_tile_ids']==sorted(set(got['selected_tile_ids'])) and len(got['selected_tile_ids'])<=data['max_tiles'])
    return name,ok,err+(' '+repr(got)[:200] if not ok else ''),got,data

def point_tile(p,x,y):
    left,bottom,right,top=p['world_bounds_m']; size=p['tile_size_m']
    if not(left<=x<right and bottom<=y<top):return None
    ix=math.floor((x-left)/size);iy=math.floor((y-bottom)/size)
    return f'{ix:03d}/{iy:03d}'

def oracle_coverage(got,p):
    pose=p['pose']; sigma=pose['bearing_uncertainty_deg']; half=p['fov_deg']/2+sigma
    selected=set(got['selected_tile_ids']); center=pose['bearing_deg']; d=p['range_m']
    if half>=180:return False, 'invalid half-angle'
    for i in range(0,101):
        theta=center-half+(2*half*i/100)
        a=math.radians(theta)
        for j in range(0,31):
            r=d*j/30
            for ox,oy in [(0,0),(pose['gps_accuracy_m']*0.95,0),(-pose['gps_accuracy_m']*0.95,0),(0,pose['gps_accuracy_m']*0.95),(0,-pose['gps_accuracy_m']*0.95)]:
                x=pose['x_m']+r*math.sin(a)+ox;y=pose['y_m']+r*math.cos(a)+oy
                tile=point_tile(p,x,y)
                if tile is not None and tile not in selected:
                    return False, f'missed witness tile={tile} at ({x:.1f},{y:.1f}) theta={theta:.1f} r={r:.1f}'
    return True, 'sampled witness coverage complete (not a proof of every continuous position)'

def main():
    script=Path(sys.argv[1]); cases=[]
    checks=[
      ('missing_source',{'source_available':False}),
      ('unauthenticated_source',{'source_provenance':'SELF_ASSERTED'}),
      ('wrong_crs',{'crs':'EPSG:4326'}),
      ('online_allowed',{'allow_network':True}),
      ('no_consent',{'operator_consent':False}),
      ('non_view_only',{'view_only':False}),
      ('claim_promotion',{'claim_ceiling':'C2_AUTHORITATIVE'}),
      ('bad_fov',{'fov_deg':0}),
      ('too_wide_fov',{'fov_deg':240}),
      ('unbounded_range',{'range_m':5000}),
      ('impossible_tile_size',{'tile_size_m':0}),
      ('zero_budget',{'max_tiles':0}),
      ('stale_fix',lambda p:p['pose'].__setitem__('timestamp_s',900)),
      ('inaccurate_fix',lambda p:p['pose'].__setitem__('gps_accuracy_m',350)),
      ('missing_camera_heading',lambda p:p['pose'].__setitem__('bearing_deg',None)),
      ('gps_course_not_camera_heading',lambda p:p['pose'].__setitem__('bearing_source','GPS_COURSE_ONLY')),
      ('invalid_heading_uncertainty',lambda p:p['pose'].__setitem__('bearing_uncertainty_deg',75)),
      ('incomplete_world_bounds',{'world_bounds_m':[-800,0,800]}),
      ('over_budget_positive',{'max_tiles':2}),
      ('future_timestamp',lambda p:p['pose'].__setitem__('timestamp_s',2000)),
    ]
    for name,patch in checks: cases.append(check_hold(script,name,patch))
    ready=[
      ('north',lambda p:None),
      ('east',lambda p:p['pose'].__setitem__('bearing_deg',90)),
      ('south',lambda p:p['pose'].__setitem__('bearing_deg',180)),
      ('west',lambda p:p['pose'].__setitem__('bearing_deg',270)),
      ('wrap_around',lambda p:p['pose'].__setitem__('bearing_deg',359)),
      ('narrow_fov',lambda p:p.__setitem__('fov_deg',25)),
      ('wide_fov',lambda p:p.__setitem__('fov_deg',140)),
    ]
    for name,patch in ready:
        n,ok,detail,got,p=check_ready(script,name,patch)
        if ok:
            covers,extra=oracle_coverage(got,p)
            ok=ok and covers
            detail+=' '+extra
        cases.append((name,ok,detail))
    _,ok1,_,a,p=check_ready(script,'again')
    _,ok2,_,b,_=check_ready(script,'again')
    cases.append(('repeat_canonical',bool(ok1 and ok2 and a==b), 'identical parsed plans across distinct invocations'))
    if isinstance(a,dict) and a.get('state')=='READY_P0_SYNTHETIC':
        selected=len(a['selected_tile_ids']); rad=p['range_m'];
        circle=sum(1 for ix in range(16) for iy in range(16)
                   if (max(-800+ix*100,-800+ix*100) < 900) and
                   math.hypot(max(abs(-800+ix*100+50)-0,0),max(abs(-800+iy*100+50)-0,0))<=rad+80)
        cases.append(('fov_reduction', selected < circle*0.75, f'selected={selected} circle_center_approx={circle}'))
    else:cases.append(('fov_reduction',False,'no ready plan'))
    for name,ok,detail in cases:print(f'{"PASS" if ok else "FAIL"} {name}: {detail}')
    passed=sum(1 for n,o,d in cases if o)
    print(f'FINAL {passed}/{len(cases)}')
    return 0 if passed==len(cases) else 1

if __name__=='__main__':
    sys.exit(main())
