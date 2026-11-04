$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Python 3.11+ installieren; dann erneut starten." }
}
& ".\.venv\Scripts\python.exe" -m pip --disable-pip-version-check install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Installation fehlgeschlagen: Proxy/Internet und Python-Version prüfen." }
& ".\.venv\Scripts\python.exe" -m pip check
if ($LASTEXITCODE -ne 0) { throw "Abhängigkeiten inkonsistent." }
& ".\.venv\Scripts\python.exe" -m orderops preflight --offline
if ($LASTEXITCODE -ne 0) { throw "Offline-Preflight fehlgeschlagen." }
Write-Host "Bereit. .env.example nach .env kopieren; kein Cloud-Aufruf wurde ausgeführt."
