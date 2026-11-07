<?php
/** NEXUS OMEGA Bodytwin public-feed reducer (Hostinger PHP CLI fallback).
 * Same public-only contract as refresh_public_feed.py. No HTTP, secrets, sensors.
 * Only run from verified Cron CLI. No online invocation.
 */
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { http_response_code(403); exit(1); }
const CEILING='C1_DESCRIPTIVE_ONLY';
const FEED_SCHEMA='nexus-bodytwin-live-feed/1';
function require_ok(bool $yes,string $why):void{if(!$yes)throw new RuntimeException('HOLD_'.$why);}
function json_file(string $path,int $max=25000):array{
  require_ok(is_file($path)&&!is_link($path),'SOURCE_MISSING_OR_SYMLINK');
  $sz=filesize($path);require_ok($sz!==false&&$sz>0&&$sz<=$max,'SOURCE_BYTES');
  $raw=file_get_contents($path);require_ok($raw!==false,'SOURCE_READ');
  try{$obj=json_decode($raw,true,64,JSON_THROW_ON_ERROR);}catch(Throwable $e){throw new RuntimeException('HOLD_SOURCE_JSON_INVALID',0,$e);}
  require_ok(is_array($obj)&&!array_is_list($obj),'SOURCE_NOT_OBJECT');
  return ['data'=>$obj,'bytes'=>$raw];
}
function exact_keys(array $a,array $keys,string $name):void{
  $present=array_keys($a);sort($present);sort($keys);
  require_ok($present===$keys,'INVALID_KEYS_'.$name);
}
function equal_set(mixed $value,array $values,string $field):void{
  require_ok(is_array($value)&&array_is_list($value)&&count($value)===count($values),'INVALID_'.$field);
  foreach($value as $v)require_ok(is_string($v),'INVALID_NONSTRING_'.$field);
  $got=$value;sort($got);sort($values);require_ok($got===$values,'INVALID_SET_'.$field);
}
function public_status(array $s):void{
  exact_keys($s,['schema','object','BODYTWIN','BODYTWIN_VALIDATED','CONSENT_BIND','TRIAL_001','layers','pipeline','invariants','claim_ceiling','claim_promotion'],'STATE');
  foreach(['schema'=>'nexus-research-bodytwin-state/1','object'=>'BODYTWIN_PUBLIC_SURFACE',
    'BODYTWIN'=>'RESEARCH_FOUNDATION_C1','BODYTWIN_VALIDATED'=>'NO','CONSENT_BIND'=>'OPEN',
    'TRIAL_001'=>'DESIGNED_NOT_EXECUTED','claim_ceiling'=>CEILING,'claim_promotion'=>false] as $k=>$v)
      require_ok($s[$k]===$v,'BAD_STATE_'.$k);
  equal_set($s['layers'],['L0','L1','L2','L3','UNKNOWN_UNOBSERVED'],'LAYERS');
  equal_set($s['pipeline'],['Capture','Normalize','Align','Refine','Metrics'],'PIPELINE');
  equal_set($s['invariants'],['RAW_NE_REFINED','PHOTOREALISM_GAIN_MAY_CAUSE_IDENTITY_LOSS','NO_PRIVATE_HUMAN_REFERENCE_MEDIA'],'INVARIANTS');
}
function public_receipts(array $r,int $now):void{
  exact_keys($r,['schema','claim_ceiling','source_object','source_date','windows','gates'],'RECEIPT');
  require_ok($r['schema']==='nexus-bodytwin-public-receipts/1'&&$r['claim_ceiling']===CEILING,'BAD_RECEIPT_SCHEMA');
  require_ok($r['source_object']==='NEXUS_OMEGA_AXIOM_R14_R2R1_WINDOWS_PORTABILITY_HARNESS_REPAIR_HANDOFF_20261107_R0','BAD_RECEIPT_PROVENANCE');
  require_ok(is_string($r['source_date'])&&preg_match('/^20\d\d-\d\d-\d\d$/',$r['source_date'])===1,'BAD_SOURCE_DATE');
  $d=DateTimeImmutable::createFromFormat('!Y-m-d',$r['source_date'],new DateTimeZone('UTC'));
  require_ok($d instanceof DateTimeImmutable&&$d->format('Y-m-d')===$r['source_date']&&$d->format('Y-m-d')<=gmdate('Y-m-d',$now),'BAD_RECEIPT_DATE');
  require_ok(is_array($r['windows'])&&!array_is_list($r['windows']),'BAD_WINDOWS');
  exact_keys($r['windows'],['status','node_pass','node_total','mutation_pass','mutation_total','schema_pass','schema_total'],'WINDOWS');
  require_ok($r['windows']['status']==='CURSOR_REPORTED_PASS_C1','UNSUPPORTED_RESULT_CLAIM');
  foreach(['node_pass','node_total','mutation_pass','mutation_total','schema_pass','schema_total'] as $k){
    require_ok(is_int($r['windows'][$k])&&$r['windows'][$k]>=0&&$r['windows'][$k]<=100000,'INVALID_COUNT_'.$k);
  }
  foreach([['node_pass','node_total'],['mutation_pass','mutation_total'],['schema_pass','schema_total']] as [$a,$b])
    require_ok($r['windows'][$a]<=$r['windows'][$b],'COUNT_OVERFLOW_'.$a);
  require_ok(is_array($r['gates'])&&!array_is_list($r['gates']),'BAD_GATES');
  exact_keys($r['gates'],['a72','r13_stage_ii','physical_imu','bodytwin_validated','consent','gate_v2'],'GATES');
  foreach(['a72'=>'SOURCE_GAP','r13_stage_ii'=>'HOLD_DEPLOY_GAP','physical_imu'=>'NOT_AUTHORIZED',
    'bodytwin_validated'=>'NO','consent'=>'OPEN','gate_v2'=>'HOLD_R9_MJS_PREREQUISITE'] as $k=>$v)
      require_ok($r['gates'][$k]===$v,'UNAUTHORIZED_GATE_'.$k);
}
function refresh(string $root):array{
  $status=json_file($root.'/research/bodytwin/state.json');
  $receipts=json_file($root.'/bodytwin/live/receipts.public.json');
  $now=time();public_status($status['data']);public_receipts($receipts['data'],$now);
  $out=$root.'/bodytwin/live/current.json';
  require_ok(!is_link($out),'OUTPUT_SYMLINK');
  $old=is_file($out)?json_file($out)['data']:null;
  if ($old!==null){
    require_ok(($old['schema']??null)===FEED_SCHEMA&&is_array($old['producer']??null)
      &&is_int($old['producer']['seq']??null)&&$old['producer']['seq']>=1,'OLD_FEED_INVALID');
    require_ok(is_string($old['producer']['run_utc']??null)&&$old['producer']['run_utc']<gmdate('Y-m-d\TH:i:s\Z',$now),'CLOCK_ROLLBACK');
  }
  $sources=[
    'bodytwin_state'=>['url'=>'/research/bodytwin/state.json','sha256'=>hash('sha256',$status['bytes'])],
    'research_receipt'=>['url'=>'/bodytwin/live/receipts.public.json','sha256'=>hash('sha256',$receipts['bytes'])]
  ];
  $changed=$old===null||($old['sources']??null)!==$sources;
  $run=gmdate('Y-m-d\TH:i:s\Z',$now);
  $s=$status['data'];$r=$receipts['data'];
  $report=[
    'schema'=>FEED_SCHEMA,'claim_ceiling'=>CEILING,'trust'=>'SELF_HOSTED_PUBLIC_C1_NOT_INDEPENDENT_WITNESS',
    'producer'=>['run_utc'=>$run,'seq'=>$old===null?1:$old['producer']['seq']+1,'interval_seconds'=>300,
      'source_changed'=>$changed,'last_change_utc'=>$changed?$run:$old['producer']['last_change_utc']],
    'sources'=>$sources,
    'bodytwin'=>['state'=>$s['BODYTWIN'],'validated'=>$s['BODYTWIN_VALIDATED'],
      'consent'=>$s['CONSENT_BIND'],'trial'=>$s['TRIAL_001']],
    'research'=>array_merge(['source_date'=>$r['source_date'],'source_object'=>$r['source_object']],$r['windows']),
    'gates'=>$r['gates']
  ];
  $json=json_encode($report,JSON_UNESCAPED_SLASHES|JSON_INVALID_UTF8_SUBSTITUTE|JSON_THROW_ON_ERROR)."\n";
  require_ok(strlen($json)<25000,'OUTPUT_SIZE');
  $tmp=tempnam(dirname($out),'.feed-');require_ok($tmp!==false,'TEMP_FAILED');
  try{
    $file=fopen($tmp,'wb');require_ok($file!==false,'OPEN_FAILED');
    $written=fwrite($file,$json);require_ok($written===strlen($json),'SHORT_WRITE');
    fflush($file);if(function_exists('fsync'))fsync($file);fclose($file);
    chmod($tmp,0644);require_ok(rename($tmp,$out),'ATOMIC_RENAME_FAILED');
  }finally{if(is_file($tmp))unlink($tmp);}
  return ['object'=>'BODYTWIN_C1_PUBLIC_FEED_TICK','state'=>'ATOMIC_PUBLIC_C1_UPDATE',
    'seq'=>$report['producer']['seq'],'source_changed'=>$changed,'bytes_sha256'=>hash('sha256',$json),'run_utc'=>$run];
}
try{
  $rootarg=null;
  foreach($argv as $i=>$arg)if($arg==='--document-root')$rootarg=$argv[$i+1]??null;
  require_ok(is_string($rootarg)&&$rootarg!=='','DOCROOT_REQUIRED');
  $root=realpath($rootarg);require_ok(is_string($root)&&is_dir($root),'DOCROOT_MISSING');
  $dir=$root.'/bodytwin/live';require_ok(is_dir($dir),'LIVE_DIR_MISSING');
  $lockpath=$dir.'/.refresh.lock';require_ok(!is_link($lockpath),'LOCK_SYMLINK');
  $lock=fopen($lockpath,'c');require_ok($lock!==false,'LOCK_OPEN');
  require_ok(flock($lock,LOCK_EX|LOCK_NB),'PARALLEL_REFRESH_DENIED');
  try{$result=refresh($root);}finally{flock($lock,LOCK_UN);fclose($lock);}
  echo json_encode($result,JSON_THROW_ON_ERROR)."\n";
}catch(Throwable $e){fwrite(STDERR,'HOLD_PUBLIC_FEED_'.$e->getMessage()."\n");exit(1);}
