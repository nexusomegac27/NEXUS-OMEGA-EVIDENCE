/* NEXUS OMEGA Gate V2 · C1 source-403 recovery candidate.
   Both transports belong to GitHub; fallback is NOT independent custody.
   Only immutable 40hex ref and allowlisted paths. Zero credentials. */
import {CONTRACT,sourcePath,digest} from './gate-core.mjs';
const HEX40=/^[0-9a-f]{40}$/;
export function pinnedRawURL(file,commit) {
  if(typeof commit!=='string'||!HEX40.test(commit))throw Error('INVALID_PINNED_COMMIT');
  const path=sourcePath(file).split('/').map(encodeURIComponent).join('/');
  return 'https://raw.githubusercontent.com/'+CONTRACT.repository+'/'+commit+'/'+path;
}
export function restRateFailure(status) {return status===403||status===429;}
export async function fetchRawPinned(file,commit,fetchFn=globalThis.fetch,timeoutMs=12000) {
  const url=pinnedRawURL(file,commit);
  const ctrl=new AbortController(),timer=setTimeout(()=>ctrl.abort(),timeoutMs);
  try{
    const res=await fetchFn(url,{method:'GET',signal:ctrl.signal,cache:'no-store',credentials:'omit',redirect:'error',mode:'cors',referrerPolicy:'no-referrer'});
    if(!res.ok)throw Error('RAW_HTTP_'+res.status);
    const declared=res.headers?.get?.('Content-Length');
    if(declared!==null&&declared!==undefined&&Number(declared)>CONTRACT.maxBytes)throw Error('RAW_CONTENT_TOO_LARGE');
    const bytes=new Uint8Array(await res.arrayBuffer());
    if(!bytes.length||bytes.length>CONTRACT.maxBytes)throw Error('RAW_BYTES_OUT_OF_BOUNDS');
    return {sha:await digest(bytes),bytes:bytes.length,raw:bytes,transport:'GITHUB_RAW_PINNED',sourceIndependence:false};
  }finally{clearTimeout(timer);}
}
export async function restOrRawPinned(file,commit,primary,fetchFn=globalThis.fetch) {
  try{
    const result=await primary(file,commit);
    return {...result,transport:'GITHUB_REST_PINNED',sourceIndependence:false};
  }catch(err){
    if(!restRateFailure(err?.status))throw err;
    // One and only one fallback. No third-party proxy, no retry storm.
    return fetchRawPinned(file,commit,fetchFn);
  }
}
