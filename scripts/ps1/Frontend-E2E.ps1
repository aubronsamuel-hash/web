Param([switch]$WithBackend)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Set-Location (Join-Path (Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")) "frontend")
cmd /c npm ci
cmd /c npx playwright install
if ($WithBackend) { $Env:E2E_WITH_BACKEND = "1" }
$Env:APP_URL = $Env:APP_URL -or "http://localhost:5173"
cmd /c npx playwright test
if ($LASTEXITCODE -ne 0){ Write-Host "[ERR] e2e KO" -ForegroundColor Red; exit 10 }
Write-Host "[OK] e2e OK" -ForegroundColor Green
exit 0
