"""Frozen independent local HTTP oracle for V11 no-redirect behavior.

Run: python frozen_alpha_handoff_no_redirect_evaluator_v11_20261102.py V11_FILE V10_FILE
No public network. Tests the transport redirect side effect; not GitHub HTTPS E2E.
Commit this evaluator before the candidate; never edit it afterwards.
"""
import base64
import hashlib
import http.server
import importlib.util
import json
import socketserver
import sys
import threading
import urllib.error
import urllib.request
from unittest.mock import patch

COMMIT = 'a' * 40
PATH = 'index/v1/latest.json'
RAW = b'{"inventory":["a","b"],"coverage_complete":true}'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def envelope(data=RAW):
    return dict(source_b64=base64.b64encode(data).decode('ascii'),
                source_sha256=hashlib.sha256(data).hexdigest(),
                source_commit=COMMIT, source_path=PATH,
                source_git_blob_sha1=blob(data))


def api(data=RAW):
    return dict(type='file', path=PATH, size=len(data), sha=blob(data),
                encoding='base64', content=base64.b64encode(data).decode('ascii'))


class HTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == '/start':
            self.send_response(302)
            self.send_header('Location', 'http://127.0.0.1:%d/sink' % self.server.server_port)
            self.end_headers()
        elif self.path == '/sink':
            self.server.sink_hits += 1
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'not an API response')
        elif self.path == '/ok':
            data = json.dumps(api()).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)


class WrappedResponse:
    """Explicitly fake same-URL response; proves a mock is not authenticated HTTPS."""
    def __init__(self, fp, original_url):
        self.fp, self.original_url = fp, original_url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.fp.close()

    @property
    def status(self):
        return self.fp.status

    def geturl(self):
        return self.original_url

    def read(self, n=-1):
        return self.fp.read(n)


def run(candidate, baseline):
    checks = []
    def record(name, passed, observation):
        checks.append(bool(passed))
        print(json.dumps(dict(test=name, pass_test=bool(passed), observed=observation), sort_keys=True))

    with HTTPServer(('127.0.0.1', 0), Handler) as server:
        server.sink_hits = 0
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        port = server.server_port
        original_urlopen = urllib.request.urlopen
        original_build = urllib.request.build_opener
        try:
            # V10's standard urlopen follows a 302 before rejecting the final URL.
            def v10_local_urlopen(req, timeout=8):
                return original_urlopen('http://127.0.0.1:%d/start' % port, timeout=timeout)
            with patch.object(urllib.request, 'urlopen', side_effect=v10_local_urlopen):
                try:
                    baseline.api_contents(COMMIT, PATH)
                except (ValueError, urllib.error.URLError):
                    pass
            record('v10_redirect_second_hop_observed', server.sink_hits == 1, server.sink_hits)
            server.sink_hits = 0

            # V11's own opener must carry NoRedirect into an actual local HTTP request.
            observed_handler = []
            def build_local_opener(*handlers):
                observed_handler.append(any(type(h).__name__ == 'NoRedirect' for h in handlers))
                real = original_build(*handlers)
                class LocalOpener:
                    def open(self, req, timeout=8):
                        return real.open('http://127.0.0.1:%d/start' % port, timeout=timeout)
                return LocalOpener()
            with patch.object(urllib.request, 'build_opener', side_effect=build_local_opener):
                try:
                    candidate.api_contents(COMMIT, PATH)
                except urllib.error.HTTPError as err:
                    record('v11_redirect_rejected_before_second_hop', err.code == 302 and server.sink_hits == 0,
                           dict(status=err.code, second_hop=server.sink_hits))
                else:
                    record('v11_redirect_rejected_before_second_hop', False, 'NO_ERROR')
            record('v11_no_redirect_handler_wired', observed_handler == [True], observed_handler)

            # The API-checking path still accepts a well-formed response, but this is a local mock.
            def build_ok_opener(*handlers):
                real = original_build(*handlers)
                class LocalOpener:
                    def open(self, req, timeout=8):
                        fp = real.open('http://127.0.0.1:%d/ok' % port, timeout=timeout)
                        return WrappedResponse(fp, req.full_url)
                return LocalOpener()
            with patch.object(urllib.request, 'build_opener', side_effect=build_ok_opener):
                response = candidate.api_contents(COMMIT, PATH)
            record('v11_mock_positive_bytes', response == api(), response.get('sha'))
            valid = candidate.check(envelope(), response, COMMIT, PATH, False)
            record('v11_mock_positive_check', valid.get('status') == 'LIVE_API_BOUND_C1_BYTES_ONLY', valid.get('status'))
            bad = candidate.check(envelope(RAW+b'x'), response, COMMIT, PATH, False)
            record('v11_modified_producer_rejected', bad.get('status') == 'NOT_COMPUTABLE', bad.get('status'))
            bad_path = candidate.check(envelope(), response, COMMIT, '../bad', False)
            record('v11_invalid_path_rejected', bad_path.get('status') == 'NOT_COMPUTABLE', bad_path.get('status'))
            fixture = candidate.check(envelope(), response, COMMIT, PATH, True)
            record('v11_fixture_label_distinct', fixture.get('status') == 'FIXTURE_BOUND_C1_BYTES_ONLY', fixture.get('status'))
            # Deliberate falsifier: a malicious injected opener can fake a 200 response.
            record('falsifier_mock_transport_not_authenticated',
                   valid.get('status') == 'LIVE_API_BOUND_C1_BYTES_ONLY' and valid.get('authenticated_actor') is False,
                   'FAKE_OPEN_ACCEPTED; LIVE_HTTPS_NOT_PROVEN')
        finally:
            server.shutdown()
            worker.join(timeout=3)
    passed = sum(checks)
    print(json.dumps(dict(passed=passed, total=len(checks), result='PASS' if passed == len(checks) else 'FAIL',
                          transport='LOOPBACK_ONLY', live_github_https='NOT_EXECUTED'), sort_keys=True))
    return 0 if passed == len(checks) else 1


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('USAGE: evaluator V11_FILE V10_FILE')
    sys.exit(run(load('candidate_v11', sys.argv[1]), load('baseline_v10', sys.argv[2])))
