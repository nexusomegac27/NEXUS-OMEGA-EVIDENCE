#!/usr/bin/env php
<?php
/**
 * Hostinger cron entry: install panel tags (idempotent) then refresh feed.
 * DOCROOT must be absolute path to public_html.
 *
 * Example:
 * /opt/alt/php83/usr/bin/php .../bodytwin/live/cron_tick.php \
 *   --document-root /home/u310432914/domains/nexus-mobile.de/public_html
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    fwrite(STDERR, "CLI_ONLY\n");
    exit(2);
}

$docroot = null;
for ($i = 1; $i < $argc; $i++) {
    if ($argv[$i] === '--document-root' && isset($argv[$i + 1])) {
        $docroot = $argv[++$i];
    }
}
if ($docroot === null || $docroot === '') {
    fwrite(STDERR, "USAGE: cron_tick.php --document-root <abs-public_html>\n");
    exit(2);
}

$dir = __DIR__;
$install = $dir . DIRECTORY_SEPARATOR . 'install_panel_tags.php';
$refresh = $dir . DIRECTORY_SEPARATOR . 'refresh_public_feed.php';

passthru(escapeshellarg(PHP_BINARY) . ' ' . escapeshellarg($install), $rc1);
passthru(
    escapeshellarg(PHP_BINARY) . ' ' . escapeshellarg($refresh)
    . ' --document-root ' . escapeshellarg($docroot),
    $rc2
);

exit(($rc1 === 0 && $rc2 === 0) ? 0 : 1);
