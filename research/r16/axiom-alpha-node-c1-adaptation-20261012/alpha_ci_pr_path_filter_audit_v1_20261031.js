'use strict';
// Isolated C1 research diagnostic. No GitHub API calls, writes, or branch protection changes.
function classify(s) {
  const fail = reason => ({status:'FAIL_CLOSED', reason});
  const sha = x => typeof x === 'string' && /^[0-9a-f]{40}$/.test(x);
  const path = x => typeof x === 'string' && x.length > 0 && !x.startsWith('/') && !x.includes('\\') && !x.split('/').some(z => z === '' || z === '.' || z === '..');
  if (!s || typeof s !== 'object' || Array.isArray(s)) return fail('root');
  if (s.repo !== 'nexusomegac27/NEXUS-OMEGA-EVIDENCE' ||
      s.pinned_workflow_commit !== 'b7adbc05c0d6b92ab77dd1fc7370f02506bfb3d9' ||
      s.inventory_commit !== '56c383b6675d47b61d1b35bb543d24a2d36de512' ||
      s.inventory_blob !== '66a330dddee79726c2384421ec2ac940a53f1225' ||
      s.pr_number !== 231 || s.pr_head !== 'a6a04f775d620e1e94cb1fd0ebcd16dfa4518c4d') return fail('pin');
  if (!Array.isArray(s.changed_files) || !s.changed_files.length || !s.changed_files.every(path) ||
      new Set(s.changed_files).size !== s.changed_files.length) return fail('changed_files');
  if (!Array.isArray(s.workflows) || s.workflows.length !== 17) return fail('workflow_count');
  let definitions=0, eligible=0, unfiltered=0, filtered=0, nonpr=0;
  const seen = new Set(), details = [];
  for (const w of s.workflows) {
    if (!w || typeof w !== 'object' || !/^\.github\/workflows\/[A-Za-z0-9_.-]+\.ya?ml$/.test(w.path || '') ||
        seen.has(w.path) || !sha(w.blob_sha) || !Number.isInteger(w.byte_length) || w.byte_length <= 0 ||
        typeof w.pull_request !== 'boolean' || w.paths_ignore !== false || !Array.isArray(w.jobs) || !w.jobs.length)
      return fail('workflow_schema');
    seen.add(w.path);
    const ids = new Set(); let names=0;
    for (const j of w.jobs) {
      if (!j || typeof j.id !== 'string' || !/^[A-Za-z][A-Za-z0-9_-]*$/.test(j.id) ||
          ids.has(j.id) || (j.name !== null && (typeof j.name !== 'string' || !j.name.trim())))
        return fail('job_schema');
      ids.add(j.id);
      if ((j.name ?? j.id) === 'validate') names++;
    }
    if (names > 1) return fail('duplicate_effective_job');
    if (!names) continue;
    if (w.paths !== null && (!Array.isArray(w.paths) || !w.paths.length ||
        !w.paths.every(p => typeof p === 'string' &&
          (p.endsWith('/**') ? path(p.slice(0,-3)) : (path(p) && !p.includes('*'))) && !/[?![\]{}]/.test(p)) ||
        new Set(w.paths).size !== w.paths.length)) return fail('path_filters');
    definitions++;
    if (!w.pull_request) {nonpr++; details.push({path:w.path,state:'NOT_PR_TRIGGERED'}); continue;}
    if (w.paths === null) {eligible++; unfiltered++; details.push({path:w.path,state:'ELIGIBLE_UNFILTERED'}); continue;}
    const matches = p => p.endsWith('/**') ? s.changed_files.some(f => f.startsWith(p.slice(0,-2))) :
      p.includes('*') ? false : s.changed_files.includes(p);
    if (w.paths.some(matches)) {eligible++; details.push({path:w.path,state:'ELIGIBLE_PATH_MATCH'});}
    else {filtered++; details.push({path:w.path,state:'EXCLUDED_BY_PATHS'});}
  }
  return {status:'PASS',workflows:s.workflows.length,validate_definitions:definitions,
          eligible,unfiltered,filtered,nonpr,details};
}
if (require.main === module) {
  try {
    const s=JSON.parse(require('fs').readFileSync(0,'utf8'));
    const result=classify(s);
    process.stdout.write(JSON.stringify(result)+'\n');
    if (result.status !== 'PASS') process.exitCode=2;
  } catch (_) {process.stdout.write(JSON.stringify({status:'FAIL_CLOSED',reason:'invalid_json'})+'\n'); process.exitCode=2;}
}
module.exports={classify};
