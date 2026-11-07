#!/usr/bin/env php
<?php
/**
 * CLI-only: idempotent insert of Bodytwin live panel tags into ../index.html
 * Relative to this script: bodytwin/live/install_panel_tags.php → bodytwin/index.html
 * MARKER: NEXUS_BODYTWIN_LIVE_PANEL_V1
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    fwrite(STDERR, "CLI_ONLY\n");
    exit(2);
}

$marker = 'NEXUS_BODYTWIN_LIVE_PANEL_V1';
$css = '<link rel="stylesheet" href="/bodytwin/live/live-panel.css" data-nexus="' . $marker . '">';
$js  = '<script type="module" src="/bodytwin/live/live-panel.js" data-nexus="' . $marker . '"></script>';
$block = "\n  <!-- {$marker} BEGIN -->\n  {$css}\n  {$js}\n  <!-- {$marker} END -->\n";

$index = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'index.html';
if (!is_file($index)) {
    fwrite(STDERR, "INDEX_ABSENT: {$index}\n");
    exit(3);
}

$html = file_get_contents($index);
if ($html === false) {
    fwrite(STDERR, "INDEX_READ_FAIL\n");
    exit(4);
}

if (strpos($html, $marker) !== false) {
    fwrite(STDOUT, "ALREADY_INSTALLED\n");
    exit(0);
}

$pos = stripos($html, '</head>');
if ($pos === false) {
    fwrite(STDERR, "HEAD_CLOSE_ABSENT\n");
    exit(5);
}

$out = substr($html, 0, $pos) . $block . substr($html, $pos);
$tmp = $index . '.tmp.' . getmypid();
if (file_put_contents($tmp, $out) === false) {
    fwrite(STDERR, "TMP_WRITE_FAIL\n");
    exit(6);
}
if (!rename($tmp, $index)) {
    @unlink($tmp);
    fwrite(STDERR, "ATOMIC_REPLACE_FAIL\n");
    exit(7);
}

fwrite(STDOUT, "INSTALLED_OK bytes=" . strlen($out) . "\n");
exit(0);
