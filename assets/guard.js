/* NEXUS R18 · read-only validation kernel. No actuator output, no estimated full-body pose. */
(function(root){
  'use strict';
  const limits = root.NEXUS_R18_JOINT_LIMITS || [];
  const fail = reason => Object.freeze({decision:'REST_REFERENCE',reason});
  function validateFrame(frame, nowMs){
    if(!frame || typeof frame !== 'object' || Array.isArray(frame)) return fail('FRAME_INVALID');
    if(frame.sensor_ok !== true) return fail('SENSOR_DROPOUT');
    const now=nowMs===undefined?Date.now():nowMs;
    if(!Number.isFinite(now) || !Number.isFinite(frame.timestamp_ms) ||
       frame.timestamp_ms>now+250 || now-frame.timestamp_ms>2000) return fail('STALE_OR_FUTURE_FRAME');
    const q=frame.quaternion;
    if(!Array.isArray(q)||q.length!==4||q.some(x=>!Number.isFinite(x))) return fail('QUATERNION_INVALID');
    const qNorm=Math.hypot(q[0],q[1],q[2],q[3]);
    if(Math.abs(qNorm-1)>0.01) return fail('QUATERNION_NORM');
    if(!frame.joint_coordinates||typeof frame.joint_coordinates!=='object'||Array.isArray(frame.joint_coordinates)) return fail('DOF_MISSING');
    if(limits.length!==23) return fail('LIMITS_NOT_FROZEN');
    for(const l of limits){
      if(!Object.prototype.hasOwnProperty.call(frame.joint_coordinates,l.name)) return fail('DOF_MISSING:'+l.name);
      const v=frame.joint_coordinates[l.name];
      if(!Number.isFinite(v)||v<l.min||v>l.max) return fail('JOINT_LIMIT:'+l.name);
    }
    return Object.freeze({decision:'SEGMENT_SIGNAL_VALID_ONLY',reason:'NO_FULL_BODY_INFERENCE_AUTHORIZED'});
  }
  const api=Object.freeze({validateFrame,limitsCount:limits.length,feedWiring:'DISABLED'});
  root.NEXUS_R18_GUARD=api;
  if(typeof module!=='undefined'&&module.exports) module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
