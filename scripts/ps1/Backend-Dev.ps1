Param(
[string]$Python = "py",
[switch]$Reinstall
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Ok($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Err($m){ Write-Host "[ERR] $m" -ForegroundColor Red }

try {
$root = Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")
Set-Location $root
if ($Reinstall -or -not (Test-Path ".venv")) {
& $Python -3.11 -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r backend\requirements.txt
} else {
. .\.venv\Scripts\Activate.ps1
}
Ok "Env installe."
python -c "import fastapi,sys;print('FastAPI',fastapi.__version__);sys.exit(0)"
exit 0
} catch {
Err $_.Exception.Message
exit 10
}
