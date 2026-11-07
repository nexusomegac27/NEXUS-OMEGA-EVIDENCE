#!/usr/bin/env php
<?php
/**
 * Hostinger cron entry: optional install panel tags (idempotent) then refresh feed.
 *
 * Hardening 20261107: skip install when Soft-View already has
 * NEXUS_BODYTWIN_LIVE_PANEL_V1 (avoids Hostinger passthru hang at RUN_INSTALL).
 * Child processes use timed proc_open (max 45s) instead of unbounded passthru.
 *
 * Hostinger alt-php: do NOT trust PHP_BINARY for child processes.
 * Prefer the absolute binary used in the cron command line.
 *
 * Example (args optional when DEFAULT_DOCROOT matches):
 * /opt/alt/php83/usr/bin/php .../bodytwin/live/cron_tick.php
 */
declare(strict_types=1);

$DEFAULT_DOCROOT = '/home/u310432914/domains/nexus-mobile.de/public_html';
$DEFAULT_PHP = '/opt/alt/php83/usr/bin/php';
$CHILD_TIMEOUT_SEC = 45;

function bt_write_receipt(string $path, array $payload): void
{
    $json = json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
    if ($json === false) {
        return;
    }
    $tmp = $path . '.tmp.' . getmypid();
    if (@file_put_contents($tmp, $json . "\n") === false) {
        return;
    }
    @rename($tmp, $path);
}

/**
 * Run external command with wall-clock timeout. Returns exit code.
 * On timeout: attempts to kill child and returns 124.
 */
function bt_run_timed(string $cmd, int $timeoutSec, string &$stdout, string &$stderr): int
{
    $stdout = '';
    $stderr = '';
    $descriptors = [
        0 => ['pipe', 'r'],
        1 => ['pipe', 'w'],
        2 => ['pipe', 'w'],
    ];
    $proc = @proc_open($cmd, $descriptors, $pipes, null, null);
    if (!is_resource($proc)) {
        $stderr = "PROC_OPEN_FAIL\n";
        return 127;
    }
    fclose($pipes[0]);
    stream_set_blocking($pipes[1], false);
    stream_set_blocking($pipes[2], false);

    $deadline = microtime(true) + $timeoutSec;
    $timedOut = false;
    while (true) {
        $status = proc_get_status($proc);
        $stdout .= (string) stream_get_contents($pipes[1]);
        $stderr .= (string) stream_get_contents($pipes[2]);
        if (!$status['running']) {
            break;
        }
        if (microtime(true) >= $deadline) {
            $timedOut = true;
            @proc_terminate($proc, 9);
            usleep(200000);
            break;
        }
        usleep(100000);
    }
    $stdout .= (string) stream_get_contents($pipes[1]);
    $stderr .= (string) stream_get_contents($pipes[2]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    $code = proc_close($proc);
    if ($timedOut) {
        $stderr .= "TIMEOUT_{$timeoutSec}S\n";
        return 124;
    }
    $statusFinal = is_int($code) ? $code : 1;
    return $statusFinal;
}

if (PHP_SAPI !== 'cli') {
    fwrite(STDERR, "CLI_ONLY\n");
    exit(2);
}

$started = gmdate('c');
$dir = __DIR__;
$receiptPath = $dir . DIRECTORY_SEPARATOR . 'cron_tick_receipt.json';
$marker = 'NEXUS_BODYTWIN_LIVE_PANEL_V1';

bt_write_receipt($receiptPath, [
    'schema' => 'nexus-bodytwin-cron-tick-receipt/1',
    'phase' => 'STARTED',
    'started_utc' => $started,
    'php_sapi' => PHP_SAPI,
    'php_version' => PHP_VERSION,
    'php_binary_const' => (string) PHP_BINARY,
    'argv' => $argv,
    'cwd' => getcwd(),
    'dir' => $dir,
    'hardening' => 'skip_install_if_marker_plus_timed_children_20261107',
]);

$docroot = null;
for ($i = 1; $i < $argc; $i++) {
    if ($argv[$i] === '--document-root' && isset($argv[$i + 1])) {
        $docroot = $argv[++$i];
    }
}
if ($docroot === null || $docroot === '') {
    $docroot = $DEFAULT_DOCROOT;
}

$php = $DEFAULT_PHP;
if (is_string(PHP_BINARY) && PHP_BINARY !== '' && is_executable(PHP_BINARY)) {
    if (strpos(PHP_BINARY, 'php') !== false) {
        $php = PHP_BINARY;
    }
}
if (!is_executable($php)) {
    $php = $DEFAULT_PHP;
}

$install = $dir . DIRECTORY_SEPARATOR . 'install_panel_tags.php';
$refresh = $dir . DIRECTORY_SEPARATOR . 'refresh_public_feed.php';
$softViewIndex = dirname($dir) . DIRECTORY_SEPARATOR . 'index.html';

echo "BODYTWIN_CRON_TICK start utc={$started} php={$php} docroot={$docroot}\n";

$installSkipped = false;
$rc1 = 0;
$installOut = '';
$installErr = '';

$already = false;
if (is_file($softViewIndex)) {
    $probe = @file_get_contents($softViewIndex);
    if (is_string($probe) && strpos($probe, $marker) !== false) {
        $already = true;
    }
}

if ($already) {
    $installSkipped = true;
    echo "SKIP_INSTALL reason=MARKER_PRESENT path={$softViewIndex}\n";
    $installOut = "SKIPPED_ALREADY_INSTALLED\n";
    $rc1 = 0;
} else {
    $cmd1 = escapeshellarg($php) . ' ' . escapeshellarg($install);
    echo "RUN_INSTALL {$cmd1}\n";
    $rc1 = bt_run_timed($cmd1, $CHILD_TIMEOUT_SEC, $installOut, $installErr);
    echo $installOut;
    if ($installErr !== '') {
        fwrite(STDERR, $installErr);
    }
}
echo "INSTALL_RC={$rc1} skipped=" . ($installSkipped ? '1' : '0') . "\n";

$refreshOut = '';
$refreshErr = '';
$cmd2 = escapeshellarg($php) . ' ' . escapeshellarg($refresh)
    . ' --document-root ' . escapeshellarg($docroot);
echo "RUN_REFRESH {$cmd2}\n";
$rc2 = bt_run_timed($cmd2, $CHILD_TIMEOUT_SEC, $refreshOut, $refreshErr);
echo $refreshOut;
if ($refreshErr !== '') {
    fwrite(STDERR, $refreshErr);
}
echo "REFRESH_RC={$rc2}\n";

$ok = ($rc1 === 0 && $rc2 === 0);
$finished = gmdate('c');
bt_write_receipt($receiptPath, [
    'schema' => 'nexus-bodytwin-cron-tick-receipt/1',
    'phase' => $ok ? 'PASS' : 'FAIL',
    'started_utc' => $started,
    'finished_utc' => $finished,
    'php_used' => $php,
    'php_binary_const' => (string) PHP_BINARY,
    'docroot' => $docroot,
    'install_rc' => $rc1,
    'install_skipped' => $installSkipped,
    'refresh_rc' => $rc2,
    'child_timeout_sec' => $CHILD_TIMEOUT_SEC,
    'argv' => $argv,
    'hardening' => 'skip_install_if_marker_plus_timed_children_20261107',
]);

echo "BODYTWIN_CRON_TICK done ok=" . ($ok ? '1' : '0') . " utc={$finished}\n";
exit($ok ? 0 : 1);
