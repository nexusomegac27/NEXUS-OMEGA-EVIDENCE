// NEXUS OMEGA · ICEBERG V1 · static, non-network, public-safe verification
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const html=readFileSync(new URL('../examples/nexus-omega-iceberg-homepage-v1.html', import.meta.url),'utf8');
test('source exists and uses German HTML semantics',()=>{assert.match(html,/<!doctype html>/i);assert.match(html,/<html lang="de">/);assert.match(html,/<main id="hauptinhalt">/);});
test('hero stays restrained and source-oriented',()=>{assert.match(html,/Wissen braucht/);assert.match(html,/Herkunft/);assert.match(html,/Offene Forschung/);assert.doesNotMatch(html,/weltweit führend|scientifically proven|validated consciousness/i);});
test('all three main public routes are visible in normal navigation',()=>{for(const href of ['https://www.nexus-mobile.de/research/','https://www.nexus-mobile.de/orbis/','https://www.nexus-mobile.de/forum/'])assert.ok(html.includes('href="'+href+'"'),href);});
test('home preserves public C1 provenance without invented live operational status',()=>{assert.match(html,/C1_DESCRIPTIVE_ONLY/);assert.match(html,/Quellen/);assert.match(html,/Validierungsgate/);assert.doesNotMatch(html,/LIVE_NODE_ONLINE|100% verified|AGENT_AUTHORIZED/);});
test('does not link 404 GBAC, private archive, internal APIs or fake satellite data',()=>{for(const bad of ['/gbac/','public_html','/internal-comm/','/api/approve','GOES-16_REAL','AO-73_BERLIN'])assert.ok(!html.includes(bad),bad);});
test('out-of-page evidence is source-linked',()=>{assert.match(html,/NEXUS-OMEGA-EVIDENCE/);assert.match(html,/status\/public-event-registry.json/);assert.match(html,/\/ai\/r14-gate\//);});
test('navigation is accessible without scripting or animation',()=>{assert.match(html,/class="nxo-skip"/);assert.match(html,/aria-label="Hauptnavigation"/);assert.match(html,/<details class="nxo-mobile">/);assert.match(html,/<summary>/);assert.match(html,/prefers-reduced-motion/);});
test('presentation is self-contained without copied third-party fonts or logos',()=>{assert.match(html,/<style>/);assert.match(html,/<\/style>/);assert.doesNotMatch(html,/<script/);assert.doesNotMatch(html,/fonts\.googleapis|palantir\.com|images\.ctfassets|cdn-cgi\/image/i);});
test('standalone preview does not create duplicate event feed, backend, timers or request channels',()=>{assert.doesNotMatch(html,/<iframe|fetch\(|setInterval\(|WebSocket|localStorage|navigator\.sendBeacon|fetch\s*:/i);});
test('existing 03 LIVE FEED is linked but not duplicated by a second source of truth',()=>{assert.match(html,/#live-feed/);assert.equal((html.match(/href="https:\/\/www\.nexus-mobile\.de\/#live-feed"/g)||[]).length,1);});
test('every same-page anchor has a matching id',()=>{let refs=[...html.matchAll(/href="#([a-z-]+)"/g)].map(x=>x[1]);for(const a of refs)assert.ok(html.includes('id="'+a+'"'),'Missing target '+a);});
test('original work is NEXUS-scoped and no global component is overwritten',()=>{assert.match(html,/<div class="nxo-home"/);assert.doesNotMatch(html,/<base href=/);});
