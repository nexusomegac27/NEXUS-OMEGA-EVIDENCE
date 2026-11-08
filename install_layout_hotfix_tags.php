<?php
/**
 * NEXUS Bodytwin P0 layout-hotfix tag installer (HTTP one-shot).
 * OBJECT: NEXUS_OMEGA_AXIOM_CURSOR_P0_BODYTWIN_LIVE_PANEL_OVERLAP_HOSTINGER_SCOPED_REPAIR_20261108_R0
 *
 * Inserts exactly two tags into ../index.html after LIVE_PANEL END / existing
 * CSS/module tags, then self-removes. Soft-View geometry / cron / feed untouched.
 *
 * Authorized tags (Issue #17):
 *   <link rel="stylesheet" href="/bodytwin/live/layout-hotfix-r0.css">
 *   <script src="/bodytwin/live/layout-hotfix-r0.js" defer></script>
 */
declare(strict_types=1);

header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex');
header('Cache-Control: no-store');

const MARKER_BEGIN = '<!-- NEXUS_BODYTWIN_LAYOUT_HOTFIX_R0 BEGIN -->';
const MARKER_END = '<!-- NEXUS_BODYTWIN_LAYOUT_HOTFIX_R0 END -->';
const LIVE_PANEL_END = '<!-- NEXUS_BODYTWIN_LIVE_PANEL END -->';
const CSS_HREF = '/bodytwin/live/layout-hotfix-r0.css';
const JS_SRC = '/bodytwin/live/layout-hotfix-r0.js';
const CSS_SHA256 = '8b5f6261e18ccc57e334f6b81063d363324322c975fe2ab3383861de7bce614f';
const JS_SHA256 = 'ed70f8aec81099ed180915ab1bceffb2cae6237c3a40418a3f1b89904241d25f';

$indexPath = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'index.html';
$selfPath = __FILE__;
$cssPath = __DIR__ . DIRECTORY_SEPARATOR . 'layout-hotfix-r0.css';
$jsPath = __DIR__ . DIRECTORY_SEPARATOR . 'layout-hotfix-r0.js';

function fail(string $code, string $detail = ''): void
{
    http_response_code(500);
    echo "FAIL\ncode={$code}\n";
    if ($detail !== '') {
        echo "detail={$detail}\n";
    }
    exit(1);
}

function sha256_file_hex(string $path): string
{
    $h = hash_file('sha256', $path);
    if ($h === false) {
        fail('HASH_FAILED', $path);
    }
    return strtolower($h);
}

if (!is_file($indexPath)) {
    fail('INDEX_MISSING', $indexPath);
}
if (!is_file($cssPath) || !is_file($jsPath)) {
    fail('HOTFIX_ASSETS_MISSING');
}

$cssHash = sha256_file_hex($cssPath);
$jsHash = sha256_file_hex($jsPath);
if ($cssHash !== CSS_SHA256) {
    fail('CSS_HASH_MISMATCH', $cssHash);
}
if ($jsHash !== JS_SHA256) {
    fail('JS_HASH_MISMATCH', $jsHash);
}

$raw = file_get_contents($indexPath);
if ($raw === false) {
    fail('INDEX_READ_FAILED');
}

if (strpos($raw, MARKER_BEGIN) !== false || strpos($raw, CSS_HREF) !== false) {
    @unlink($selfPath);
    echo "ALREADY_INSTALLED\n";
    echo "index_bytes=" . strlen($raw) . "\n";
    echo "css_sha256={$cssHash}\n";
    echo "js_sha256={$jsHash}\n";
    echo "self_removed=" . (is_file($selfPath) ? 'NO' : 'YES') . "\n";
    exit(0);
}

$block = MARKER_BEGIN . "\n"
    . '<link rel="stylesheet" href="' . CSS_HREF . '">' . "\n"
    . '<script src="' . JS_SRC . '" defer></script>' . "\n"
    . MARKER_END . "\n";

$pos = strpos($raw, LIVE_PANEL_END);
if ($pos === false) {
    // Fallback: insert before </head>
    $headClose = stripos($raw, '</head>');
    if ($headClose === false) {
        fail('NO_INSERT_ANCHOR');
    }
    $new = substr($raw, 0, $headClose) . $block . substr($raw, $headClose);
} else {
    $lineEnd = strpos($raw, "\n", $pos);
    if ($lineEnd === false) {
        $lineEnd = $pos + strlen(LIVE_PANEL_END);
    } else {
        $lineEnd += 1;
    }
    $new = substr($raw, 0, $lineEnd) . $block . substr($raw, $lineEnd);
}

$tmp = $indexPath . '.layout-hotfix.tmp';
if (file_put_contents($tmp, $new) === false) {
    fail('INDEX_WRITE_TMP_FAILED');
}
if (!rename($tmp, $indexPath)) {
    @unlink($tmp);
    fail('INDEX_RENAME_FAILED');
}

@unlink($selfPath);

$after = file_get_contents($indexPath);
$afterBytes = ($after === false) ? -1 : strlen($after);
$hasCss = ($after !== false && strpos($after, CSS_HREF) !== false);
$hasJs = ($after !== false && strpos($after, JS_SRC) !== false);

echo "PASS\n";
echo "index_bytes_before=" . strlen($raw) . "\n";
echo "index_bytes_after={$afterBytes}\n";
echo "has_css_tag=" . ($hasCss ? 'YES' : 'NO') . "\n";
echo "has_js_tag=" . ($hasJs ? 'YES' : 'NO') . "\n";
echo "css_sha256={$cssHash}\n";
echo "js_sha256={$jsHash}\n";
echo "self_removed=" . (is_file($selfPath) ? 'NO' : 'YES') . "\n";
exit(0);
