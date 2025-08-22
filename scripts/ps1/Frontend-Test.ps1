$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Set-Location (Join-Path (Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")) "frontend")
cmd /c npm ci
cmd /c npm run lint
if ($LASTEXITCODE -ne 0){ exit 10 }
cmd /c npm run typecheck
if ($LASTEXITCODE -ne 0){ exit 10 }
cmd /c npm test
if ($LASTEXITCODE -ne 0){ exit 10 }
Write-Host "[OK] tests/lint/typecheck OK" -ForegroundColor Green
exit 0
