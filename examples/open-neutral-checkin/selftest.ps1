# G7 Windows wrapper — no install; requires Node 20+
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $Root '..\..')
node (Join-Path $Root 'selftest.mjs')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
