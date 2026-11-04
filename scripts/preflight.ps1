param([switch]$Cloud)
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($Cloud) {
    & ".\.venv\Scripts\python.exe" -m orderops preflight --allow-cloud
} else {
    & ".\.venv\Scripts\python.exe" -m orderops preflight --offline
}
exit $LASTEXITCODE
