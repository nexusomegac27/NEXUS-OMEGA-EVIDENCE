/**
 * Loopback-only HTTP surface for Open Neutral Check-in.
 * Bind: 127.0.0.1 only (all-interfaces bind refused). PUBLIC_EXTERNAL_WRITE_API = HOLD.
 */
import http from 'node:http';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import {
  processCheckin,
  healthPayload,
  createLedger,
  MAX_BODY_BYTES,
} from './open-neutral-checkin.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOST = process.env.NEXUS_CHECKIN_HOST || '127.0.0.1';
const PORT = Number(process.env.NEXUS_CHECKIN_PORT || 18765);

if (HOST !== '127.0.0.1' && HOST !== 'localhost') {
  console.error('REFUSE: only 127.0.0.1/localhost bind allowed (PUBLIC_EXTERNAL_WRITE_API=HOLD)');
  process.exit(2);
}

const ledger = createLedger(join(__dirname, '.runtime'));
const rateBucket = { hits: [] };

function send(res, code, obj, type = 'application/json; charset=utf-8') {
  const body = typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2);
  res.writeHead(code, {
    'Content-Type': type,
    'Cache-Control': 'no-store',
    'X-Nexus-Claim-Ceiling': 'C1_DESCRIPTIVE_ONLY',
    'X-Nexus-Public-Write': 'HOLD',
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > MAX_BODY_BYTES) {
        reject(Object.assign(new Error('BODY_TOO_LARGE'), { code: 'BODY_TOO_LARGE' }));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || '/', `http://${HOST}:${PORT}`);

  if (req.method === 'GET' && (url.pathname === '/health' || url.pathname === '/api/v1/health')) {
    return send(res, 200, healthPayload(HOST));
  }

  if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/ui' || url.pathname === '/ui/')) {
    try {
      const html = readFileSync(join(__dirname, 'ui', 'index.html'), 'utf8');
      return send(res, 200, html, 'text/html; charset=utf-8');
    } catch {
      return send(res, 500, { error: 'UI_MISSING' });
    }
  }

  if (req.method === 'POST' && (url.pathname === '/checkin' || url.pathname === '/api/v1/checkin')) {
    try {
      const buf = await readBody(req);
      const result = processCheckin(buf.toString('utf8'), { ledger, rateBucket });
      const code = result.status === 'STAGED_UNTRUSTED' ? 202
        : result.status === 'DUPLICATE' ? 200
          : result.status === 'DENIED' && result.deny_code === 'RATE_LIMITED' ? 429
            : 400;
      return send(res, code, result);
    } catch (e) {
      if (e && e.code === 'BODY_TOO_LARGE') {
        return send(res, 413, processCheckin(Buffer.alloc(MAX_BODY_BYTES + 1), { ledger, rateBucket }));
      }
      return send(res, 500, { status: 'DENIED', deny_code: 'SERVER_ERROR' });
    }
  }

  send(res, 404, { error: 'NOT_FOUND', hint: 'GET /health | GET /ui | POST /checkin' });
});

const isMain = process.argv[1]
  && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  server.listen(PORT, HOST, () => {
    console.log(JSON.stringify({
      listening: `http://${HOST}:${PORT}`,
      public_external_write_api: 'HOLD',
      claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    }));
  });
}

export { server, HOST, PORT, ledger, rateBucket };
