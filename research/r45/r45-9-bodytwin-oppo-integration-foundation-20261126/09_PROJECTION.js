// Offline, toy source-time and public projection diagnostics, no actual device/HTTP.
function run(){
 const tests=[];
 function check(id,v){tests.push({id,pass:v===true});if(v!==true)throw Error(id)}
 const parseNs=x=>typeof x==="string"&&/^(0|[1-9][0-9]*)$/.test(x)?BigInt(x):null;
 function freshness(event,now,ttl){
   if(!event||!now||!Number.isFinite(ttl)||ttl<0||![...event,...now].every(Number.isFinite)||event[0]>event[1]||now[0]>now[1])return "UNKNOWN";
   let lo=now[0]-event[1],hi=now[1]-event[0];
   return lo>=0&&hi<=ttl?"FRESH":lo>ttl?"STALE":"AMBIGUOUS";
 }
 function projection(x,now){
   // intentionally minimal synthetic schema, no production declassification.
   if(x.classification!=="SYNTHETIC"||x.claim_ceiling!=="C1_DESCRIPTIVE_ONLY"||!Number.isFinite(x.metric))return null;
   return {schema_version:"toy-v0",classification:"SYNTHETIC",claim_ceiling:"C1_DESCRIPTIVE_ONLY",freshness:freshness(x.event,now,30),metric:x.metric};
 }
 let a=parseNs("9007199254740992"),b=parseNs("9007199254740993");
 check("decimal_ns_distinct",b-a===1n);check("js_number_collides",Number(a)===Number(b));check("numeric_ns_rejected",parseNs(9007199254740992)===null);
 check("same_boot_clock_not_utc",parseNs("1000")===parseNs("1000")); // equal numeric values give no cross-device offset information
 check("fresh",freshness([100,102],[110,112],30)==="FRESH");
 check("stale",freshness([100,102],[135,136],30)==="STALE");
 check("ambiguous",freshness([100,102],[130,132],30)==="AMBIGUOUS");
 check("future",freshness([100,102],[95,96],30)==="AMBIGUOUS");
 check("clock_unknown",freshness(null,[110,112],30)==="UNKNOWN");
 const raw={classification:"SYNTHETIC",claim_ceiling:"C1_DESCRIPTIVE_ONLY",event:[100,102],metric:1,raw_device:"private-placeholder",raw_location:"private-placeholder"};
 let pub=projection(raw,[135,136]);
 check("allowlist_only",!Object.hasOwn(pub,"raw_device")&&!Object.hasOwn(pub,"raw_location")&&!Object.hasOwn(pub,"event"));
 check("304_not_fresh",projection(raw,[140,141]).freshness==="STALE");
 check("real_data_not_released",projection({...raw,classification:"VERIFIED_DERIVED"},[110,112])===null);
 check("promotion_denied",projection({...raw,claim_ceiling:"C2"},[110,112])===null);
 check("nonfinite_denied",projection({...raw,metric:NaN},[110,112])===null);
 return {tests,matched:tests.length,example_public:pub,formal_credit:false,limits:"toy projection, no full schema or privacy proof; clock equality example only, no sync estimation"};
}
const result=run();if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
