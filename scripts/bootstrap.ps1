$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Install Python 3.11+; then try again." }
}
& ".\.venv\Scripts\python.exe" -m pip --disable-pip-version-check install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Installation failed: check proxy/Internet and Python version." }
& ".\.venv\Scripts\python.exe" -m pip check
if ($LASTEXITCODE -ne 0) { throw "Inconsistent dependencies." }
& ".\.venv\Scripts\python.exe" -m orderops preflight --offline
if ($LASTEXITCODE -ne 0) { throw "Offline preflight failed." }
Write-Host "Ready. Copy .env.example to .env only if absent; no cloud call was made."
