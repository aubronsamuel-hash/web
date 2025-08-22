Param()
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Ok($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Err($m){ Write-Host "[ERR] $m" -ForegroundColor Red }

try {
    $root = Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")
    Set-Location $root
    . ..venv\Scripts\Activate.ps1
    if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" -Force }
    if (-not (Test-Path "backend\alembic.ini")) { throw "alembic.ini manquant." }
    cmd /c "alembic -c backend\alembic.ini upgrade head"
    if ($LASTEXITCODE -ne 0) { throw "alembic upgrade a echoue." }
    Ok "Migrations appliquees."
    exit 0
} catch {
    Err $_.Exception.Message
    exit 10
}

