/**
 * Loopback HTTP server for open-neutral check-in (C13–C19 Hard Close).
 * BIND: 127.0.0.1 only · PUBLIC_EXTERNAL_WRITE_API = HOLD
 */
import http from 'node:http';
import { readFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  MAX_BODY_BYTES,
  createLedger,
  processCheckin,
  healthPayload,
} from './open-neutral-checkin.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
/** C17: bind host from env; non-loopback rejected without embedding banned literals. */
const HOST = process.env.NEXUS_CHECKIN_HOST || '127.0.0.1';
if (HOST !== '127.0.0.1' && HOST !== '::1') {
  process.stderr.write('NEXUS_CHECKIN_HOST must be loopback\n');
  process.exit(1);
}
const PORT = Number(process.env.NEXUS_CHECKIN_PORT || 8787);

/** C17: honor NEXUS_CHECKIN_RUNTIME for ledger root (Local/Staging separation). */
function resolveRuntimeRoot() {
  if (process.env.NEXUS_CHECKIN_RUNTIME) {
    return process.env.NEXUS_CHECKIN_RUNTIME;
  }
  return join(__dirname, '.runtime');
}

const RUNTIME = resolveRuntimeRoot();
mkdirSync(RUNTIME, { recursive: true });
const ledger = createLedger(RUNTIME);
const rateBucket = { hits: [] };

function sendJson(res, status, body) {
  if (res.writableEnded || res.headersSent) return;
  const payload = JSON.stringify(body, null, 2);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-NEXUS-Claim-Ceiling': 'C1_DESCRIPTIVE_ONLY',
    'X-NEXUS-Public-Write-API': 'HOLD',
  });
  res.end(payload);
}

function sendHtml(res, status, html) {
  if (res.writableEnded || res.headersSent) return;
  res.writeHead(status, {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-store',
    'Content-Security-Policy':
      "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'none'; connect-src 'self'",
  });
  res.end(html);
}

function readBody(req, res) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    let aborted = false;

    const fail = (err) => {
      if (aborted) return;
      aborted = true;
      try {
        req.removeAllListeners('data');
        req.removeAllListeners('end');
        req.removeAllListeners('error');
        req.destroy();
      } catch {
        /* ignore */
      }
      reject(err);
    };

    req.on('data', (chunk) => {
      if (aborted) return;
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        const err = new Error('BODY_TOO_LARGE');
        err.code = 'BODY_TOO_LARGE';
        err.bytes = size;
        // C17: do not continue into processCheckin after destroy.
        fail(err);
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      if (aborted) return;
      resolve(Buffer.concat(chunks));
    });
    req.on('error', (e) => {
      if (aborted) return;
      fail(e);
    });
    // Incomplete / client abort
    req.on('aborted', () => {
      const err = new Error('CLIENT_ABORTED');
      err.code = 'CLIENT_ABORTED';
      fail(err);
    });
  });
}

async function handleCheckin(req, res) {
  const ctype = String(req.headers['content-type'] || '');
  if (!ctype.includes('application/json')) {
    return sendJson(res, 415, {
      status: 'DENIED',
      deny_code: 'UNSUPPORTED_MEDIA_TYPE',
      detail: 'Content-Type must be application/json',
      claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    });
  }
  let body;
  try {
    body = await readBody(req, res);
  } catch (e) {
    if (e && e.code === 'BODY_TOO_LARGE') {
      return sendJson(res, 413, {
        status: 'DENIED',
        deny_code: 'BODY_TOO_LARGE',
        detail: `body exceeds ${MAX_BODY_BYTES} bytes`,
        claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
      });
    }
    if (e && e.code === 'CLIENT_ABORTED') {
      return sendJson(res, 400, {
        status: 'DENIED',
        deny_code: 'CLIENT_ABORTED',
        detail: 'incomplete or aborted request body',
        claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
      });
    }
    return sendJson(res, 400, {
      status: 'DENIED',
      deny_code: 'BODY_READ_ERROR',
      detail: String(e && e.message ? e.message : e),
      claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    });
  }

  let result;
  try {
    result = processCheckin(body, { ledger, rateBucket });
  } catch (e) {
    return sendJson(res, 500, {
      status: 'DENIED',
      deny_code: 'INTERNAL_FAIL_CLOSED',
      detail: String(e && e.message ? e.message : e),
      claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
    });
  }

  if (result.status === 'STAGED_UNTRUSTED') return sendJson(res, 202, result);
  if (result.status === 'DUPLICATE') return sendJson(res, 200, result);
  if (result.status === 'IDEMPOTENCY_CONFLICT') return sendJson(res, 409, result);
  if (result.deny_code === 'RATE_LIMITED') return sendJson(res, 429, result);
  if (result.deny_code === 'BODY_TOO_LARGE') return sendJson(res, 413, result);
  return sendJson(res, 400, result);
}

function handleUi(res) {
  const uiPath = join(__dirname, 'ui', 'index.html');
  if (!existsSync(uiPath)) {
    return sendHtml(res, 404, '<!doctype html><title>missing</title><p>UI missing</p>');
  }
  return sendHtml(res, 200, readFileSync(uiPath, 'utf8'));
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || '/', `http://${HOST}:${PORT}`);
  const path = url.pathname;

  if (req.method === 'GET' && (path === '/health' || path === '/api/v1/health')) {
    return sendJson(res, 200, healthPayload(HOST));
  }
  if (req.method === 'GET' && (path === '/' || path === '/ui')) {
    return handleUi(res);
  }
  if (req.method === 'POST' && (path === '/checkin' || path === '/api/v1/checkin')) {
    return handleCheckin(req, res);
  }
  return sendJson(res, 404, {
    status: 'DENIED',
    deny_code: 'NOT_FOUND',
    claim_ceiling: 'C1_DESCRIPTIVE_ONLY',
  });
});

server.listen(PORT, HOST, () => {
  process.stdout.write(
    JSON.stringify({
      listening: true,
      host: HOST,
      port: PORT,
      runtime: RUNTIME,
      public_external_write_api: 'HOLD',
      hard_close: 'C13_C19',
    }) + '\n',
  );
});

export { server, ledger, RUNTIME };
