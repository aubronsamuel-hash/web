$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Must($code, $cmd){
Write-Host "== $cmd" -ForegroundColor Cyan
cmd /c $cmd
if ($LASTEXITCODE -ne $code) {
Write-Host "[FAIL] code $LASTEXITCODE attendu $code" -ForegroundColor Red
exit 10
}
}

. .\.venv\Scripts\Activate.ps1
$Env:PYTHONPATH = "backend"

Must 0 "python -m ruff check backend"
Must 0 "python -m mypy backend"
Must 0 "pytest -q --cov=backend"

Write-Host "[OK] Tests backend passes" -ForegroundColor Green
exit 0
