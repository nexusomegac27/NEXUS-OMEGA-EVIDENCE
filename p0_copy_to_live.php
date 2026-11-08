<?php
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
$root = dirname(__DIR__); // bodytwin when script is in live_p0_stage
$src = __DIR__;
$dst = $root . DIRECTORY_SEPARATOR . 'live';
$ok = true;
$lines = [];
foreach (['layout-hotfix-r0.css', 'layout-hotfix-r0.js'] as $name) {
    $from = $src . DIRECTORY_SEPARATOR . $name;
    $to = $dst . DIRECTORY_SEPARATOR . $name;
    if (!is_file($from)) {
        $lines[] = "MISSING_SRC $name";
        $ok = false;
        continue;
    }
    if (!@copy($from, $to)) {
        $lines[] = "COPY_FAIL $name";
        $ok = false;
        continue;
    }
    $lines[] = 'COPIED ' . $name . ' ' . filesize($to) . ' ' . hash_file('sha256', $to);
}
$marker = $dst . DIRECTORY_SEPARATOR . '.p0_hotfix_fetch.ok';
@file_put_contents($marker, date('c') . "\n");
$lines[] = $ok ? 'PASS' : 'FAIL';
echo implode("\n", $lines), "\n";