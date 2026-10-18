"""NEXUS OMEGA R15 synthetic-only conservative GPS/FOV tile preflight.

STANDALONE DESIGN PROBE, NOT GPS INGESTION, 3D FRUSTUM, DATASET VALIDATION,
BROWSER OFFLINE PROOF, PUBLICATION AUTHORITY, OR SCIENTIFIC MEASUREMENT.

Positions are in an invented 2-D local tangent plane in metres. The caller
MUST NOT submit real GPS or genuine WGS84 coordinates. An actual GIS deployment
would require a source-anchored CRS/vertical datum and independently validated
location/orientation pipeline outside this component.
"""
import json
import math
import sys
from pathlib import Path

class StrictError(ValueError):
    pass

def no_dupes(items):
    d={}
    for key,val in items:
        if key in d:raise StrictError('duplicate_json_key')
        d[key]=val
    return d

def no_constants(token):
    raise StrictError('nonfinite_constant')

def parse_float(token):
    value=float(token)
    if not math.isfinite(value):raise StrictError('floating_point_overflow')
    return value

def num(value,minv,maxv):
    return type(value) in (float,int) and math.isfinite(value) and minv<=value<=maxv

def orientation(bearing):
    return math.sin(math.radians(bearing)),math.cos(math.radians(bearing))

def projections(points,axis):
    return [x*axis[0]+y*axis[1] for x,y in points]

def intersects_triangle_aabb(triangle,rect):
    x0,y0,x1,y1=rect
    corners=((x0,y0),(x1,y0),(x1,y1),(x0,y1))
    axes=[(1,0),(0,1)]
    for i in range(3):
        x,y=triangle[i]; xx,yy=triangle[(i+1)%3]
        dx,dy=xx-x,yy-y
        axes.append((-dy,dx))
    for axis in axes:
        tri=projections(triangle,axis);box=projections(corners,axis)
        if max(tri)<min(box)-1e-8 or max(box)<min(tri)-1e-8:
            return False
    return True

def sector_intersects_aabb(x,y,bearing,half_fov,range_m,rect):
    """Conservative circumscribed fan; no invisible tile is guaranteed excluded."""
    start=bearing-half_fov
    end=bearing+half_fov
    steps=math.ceil((end-start)/5)
    step=(end-start)/steps
    radius=range_m/math.cos(math.radians(step/2))
    origin=(x,y)
    for i in range(steps):
        sx,sy=orientation(start+i*step)
        ex,ey=orientation(start+(i+1)*step)
        tri=(origin,(x+radius*sx,y+radius*sy),(x+radius*ex,y+radius*ey))
        if intersects_triangle_aabb(tri,rect): return True
    return False

def fail(reason):
    return {'state':'HOLD_SCOPED','reason':reason,'selected_tile_ids':[],
            'network_requests':0,'eligible_for_authoritative_claim':False,
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def plan(p):
    if not isinstance(p,dict):return fail('input_not_object')
    if p.get('profile')!='R15_SYNTHETIC_ENU_ONLY':return fail('profile_not_synthetic')
    if p.get('source_ref')!='synthetic://manifest-v1' or p.get('source_provenance')!='LOCAL_VERIFIED' or p.get('source_available') is not True:
        return fail('source_fixture_unavailable')
    if p.get('crs')!='LOCAL_ENU_SYNTHETIC':return fail('unsupported_crs_no_real_gps_ingest')
    if p.get('allow_network') is not False:return fail('network_not_disabled')
    if p.get('operator_consent') is not True:return fail('no_consent')
    if p.get('view_only') is not True:return fail('write_capability_not_allowed')
    if p.get('claim_ceiling')!='C1_DESCRIPTIVE_ONLY':return fail('claim_promotion_prohibited')
    pose=p.get('pose')
    if not isinstance(pose,dict):return fail('missing_pose')
    # MUTANT: do not verify camera-bearing source
    for key,a,b in [('x_m',-10000,10000),('y_m',-10000,10000),('bearing_deg',0,359.999999),
                    ('bearing_uncertainty_deg',0,30),('gps_accuracy_m',0.01,100)]:
        if not num(pose.get(key),a,b):return fail('invalid_pose_'+key)
    if not num(pose.get('timestamp_s'),0,1e15) or not num(p.get('now_s'),0,1e15) or not num(p.get('max_age_s'),0.01,120):
        return fail('invalid_time')
    if pose['timestamp_s']>p['now_s'] or p['now_s']-pose['timestamp_s']>p['max_age_s']:
        return fail('stale_or_future_pose')
    if not num(p.get('fov_deg'),1,160):return fail('bad_fov')
    if not num(p.get('range_m'),5,1200):return fail('range_out_of_scope')
    if not num(p.get('tile_size_m'),10,1000):return fail('bad_tile_size')
    if not num(p.get('max_tiles'),1,1000) or int(p['max_tiles'])!=p['max_tiles']:return fail('bad_budget')
    wb=p.get('world_bounds_m')
    if not isinstance(wb,list) or len(wb)!=4 or not all(num(x,-20000,20000) for x in wb):return fail('bad_world_bounds')
    x0,y0,x1,y1=wb
    ncols=(x1-x0)/p['tile_size_m'];nrows=(y1-y0)/p['tile_size_m']
    if not (0<ncols<=100 and 0<nrows<=100 and ncols.is_integer() and nrows.is_integer()):return fail('invalid_grid_shape')
    # Inflate the tile AABB by positional uncertainty. This admits all camera
    # offsets in the stated circular accuracy radius, at the cost of extra tiles.
    acc=pose['gps_accuracy_m']; half=p['fov_deg']/2+pose['bearing_uncertainty_deg']
    if half>=179:return fail('uncertain_heading_exceeds_sector')
    ids=[]
    for ix in range(int(ncols)):
        for iy in range(int(nrows)):
            left=x0+ix*p['tile_size_m'];bottom=y0+iy*p['tile_size_m']
            box=(left-acc,bottom-acc,left+p['tile_size_m']+acc,bottom+p['tile_size_m']+acc)
            if sector_intersects_aabb(pose['x_m'],pose['y_m'],pose['bearing_deg'],half,p['range_m'],box):
                ids.append(f'{ix:03d}/{iy:03d}')
                if len(ids)>p['max_tiles']:return fail('visible_tiles_exceed_budget_no_truncation')
    ids.sort()
    return {'state':'READY_P0_SYNTHETIC','reason':'visual_tile_plan_only_untrusted_by_default',
            'selected_tile_ids':ids,'network_requests':0,'eligible_for_authoritative_claim':False,
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY','tile_size_m':p['tile_size_m'],
            'selection_model':'2D_CONSERVATIVE_SECTOR_NO_3D_OCCLUSION',
            'crs':p['crs'],'privacy':'SYNTHETIC_ONLY_NO_REAL_LOCATION'}

def main():
    if len(sys.argv)!=2:
        print(json.dumps(fail('usage_one_json_argument'),sort_keys=True,separators=(',',':')))
        return 2
    try:
        raw=Path(sys.argv[1]).read_text(encoding='utf-8')
        p=json.loads(raw,object_pairs_hook=no_dupes,parse_constant=no_constants,parse_float=parse_float)
        output=plan(p)
    except (OSError,ValueError,TypeError,OverflowError,ZeroDivisionError) as exc:
        output=fail('malformed_input_'+type(exc).__name__)
    print(json.dumps(output,sort_keys=True,ensure_ascii=True,separators=(',',':')))
    return 0 if output['state']=='READY_P0_SYNTHETIC' else 2
if __name__=='__main__':
    sys.exit(main())
