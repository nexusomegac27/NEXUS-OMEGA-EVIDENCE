"""R15 AXIOM post-hoc supplementary synthetic 2D coverage check.
Not a frozen-before-candidate test, not a full mathematical proof, not GPS or 3D.
Uses independent point-sampling witnesses; never authorizes runtime/claims.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path


def load_module(path):
    spec=importlib.util.spec_from_file_location('candidate_r15',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def case(seed,i):
    rng=random.Random((seed<<12)+i)
    d={
      'profile':'R15_SYNTHETIC_ENU_ONLY','source_ref':'synthetic://manifest-v1',
      'source_provenance':'LOCAL_VERIFIED','source_available':True,'crs':'LOCAL_ENU_SYNTHETIC',
      'pose': {'x_m':rng.uniform(-190,190),'y_m':rng.uniform(-190,190),
        'bearing_deg': rng.uniform(0,359.9),'bearing_source':'DEVICE_HEADING_VERIFIED',
        'bearing_uncertainty_deg':rng.uniform(0,20),'gps_accuracy_m':rng.uniform(0.1,25),
        'timestamp_s':990},
      'now_s':1000,'max_age_s':30,'tile_size_m':40,'world_bounds_m':[-320,-320,320,320],
      'fov_deg':rng.uniform(10,110),'range_m':rng.uniform(80,250),'max_tiles':400,
      'allow_network':False,'operator_consent':True,'view_only':True,
      'claim_ceiling':'C1_DESCRIPTIVE_ONLY',
    }
    return d


def independent_sample_coverage(p,selected):
    """Point witnesses across the full uncertainty-expanded circular sector.
    The witness shape uses point inclusion and index arithmetic, NOT the
    candidate's triangle-vs-AABB intersection or sector predicate.
    """
    ix0,iy0,ix1,iy1=p['world_bounds_m'];size=p['tile_size_m'];pose=p['pose']
    center=pose['bearing_deg'];half=p['fov_deg']/2+pose['bearing_uncertainty_deg']
    radius=p['range_m'];acc=pose['gps_accuracy_m']
    gridpts=0
    for step in range(27):
        deg=center-half+2*half*step/26
        theta=math.radians(deg)
        sx,sy=math.sin(theta),math.cos(theta)
        for ir in range(16):
            r=radius*ir/15
            # Extra samples at the circle boundary, which are the hardest.
            for ox,oy in ((0,0),(acc,0),(-acc,0),(0,acc),(0,-acc),
                          (acc/math.sqrt(2),acc/math.sqrt(2)),
                          (-acc/math.sqrt(2),-acc/math.sqrt(2))):
                x=pose['x_m']+r*sx+ox;y=pose['y_m']+r*sy+oy
                if ix0<=x<ix1 and iy0<=y<iy1:
                    tile=f'{math.floor((x-ix0)/size):03d}/{math.floor((y-iy0)/size):03d}'
                    gridpts+=1
                    if tile not in selected:
                        return False, {'missing_tile':tile,'x':x,'y':y,'heading_deg':deg,'distance_m':r,'sampled':gridpts}
    return True, {'sampled':gridpts}


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--candidate',required=True);pa.add_argument('--output',required=True);args=pa.parse_args()
    candidate=load_module(Path(args.candidate))
    seed=20261018;count=64;passes=0;points=0;errors=[]
    for i in range(count):
        p=case(seed,i);res=candidate.plan(p)
        if res['state']!='READY_P0_SYNTHETIC':errors.append({'case':i,'result':res});continue
        ids=set(res['selected_tile_ids'])
        if res['selected_tile_ids'] != sorted(ids):errors.append({'case':i,'error':'ids not sorted/unique'});continue
        ok,detail=independent_sample_coverage(p,ids)
        points+=detail.get('sampled',0)
        if ok:passes+=1
        else: errors.append({'case':i,'detail':detail})
    out={'profile':'AXIOM_RETROSPECTIVE_INDEPENDENT_2D_POINT_ORACLE_SYNTHETIC_ONLY',
         'seed':seed,'sampled_cases':count,'passed_cases':passes,'sampled_points':points,
         'candidate_source':Path(args.candidate).name,'failures':errors,
         'claim':'No missed point among sampled synthetic witnesses only; NOT a full coverage proof or 3D/offline validation.'}
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(f'R15 SUPPLEMENTAL 2D WITNESS: {passes}/{count} cases, {points} sampled points, misses {len(errors)}')
    return 0 if not errors else 1

if __name__=='__main__':raise SystemExit(main())
