$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Set-Location (Join-Path (Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")) "frontend")
cmd /c npm ci
cmd /c npm run build
if ($LASTEXITCODE -ne 0){ Write-Host "[ERR] build KO" -ForegroundColor Red; exit 10 }
Write-Host "[OK] build OK" -ForegroundColor Green
exit 0
