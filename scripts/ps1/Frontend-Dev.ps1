Param([switch]$Reinstall)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Ok($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Err($m){ Write-Host "[ERR] $m" -ForegroundColor Red }

try {
$root = Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")
Set-Location (Join-Path $root "frontend")
if ($Reinstall -or -not (Test-Path "node_modules")) { cmd /c npm ci }
Ok "Deps installees."
cmd /c npm run dev
exit 0
} catch { Err $_.Exception.Message; exit 10 }
