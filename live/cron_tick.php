#!/usr/bin/env php
<?php
/**
 * Hostinger cron entry: install panel tags (idempotent) then refresh feed.
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

if (PHP_SAPI !== 'cli') {
    fwrite(STDERR, "CLI_ONLY\n");
    exit(2);
}

$started = gmdate('c');
$dir = __DIR__;
$receiptPath = $dir . DIRECTORY_SEPARATOR . 'cron_tick_receipt.json';

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
    // Prefer cron-invoked binary when it looks like alt-php.
    if (strpos(PHP_BINARY, 'php') !== false) {
        $php = PHP_BINARY;
    }
}
if (!is_executable($php)) {
    $php = $DEFAULT_PHP;
}

$install = $dir . DIRECTORY_SEPARATOR . 'install_panel_tags.php';
$refresh = $dir . DIRECTORY_SEPARATOR . 'refresh_public_feed.php';

echo "BODYTWIN_CRON_TICK start utc={$started} php={$php} docroot={$docroot}\n";

$cmd1 = escapeshellarg($php) . ' ' . escapeshellarg($install);
echo "RUN_INSTALL {$cmd1}\n";
passthru($cmd1, $rc1);
echo "INSTALL_RC={$rc1}\n";

$cmd2 = escapeshellarg($php) . ' ' . escapeshellarg($refresh)
    . ' --document-root ' . escapeshellarg($docroot);
echo "RUN_REFRESH {$cmd2}\n";
passthru($cmd2, $rc2);
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
    'refresh_rc' => $rc2,
    'argv' => $argv,
]);

echo "BODYTWIN_CRON_TICK done ok=" . ($ok ? '1' : '0') . " utc={$finished}\n";
exit($ok ? 0 : 1);
