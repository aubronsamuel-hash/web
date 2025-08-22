Param()
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Load-DotEnv($path){
if (-not (Test-Path $path)) { return }
Get-Content $path | Where-Object { $_ -and ($_ -notmatch '^\s*#') } | ForEach-Object {
$kv = $_.Split('=',2)
if ($kv.Length -eq 2) {
$name = $kv[0].Trim()
$val = $kv[1].Trim()
[Environment]::SetEnvironmentVariable($name, $val)
}
}
}

try {
$root = Resolve-Path (Join-Path (Split-Path $PSCommandPath) "....")
Set-Location $root
. .\.venv\Scripts\Activate.ps1
if (Test-Path ".env") { Load-DotEnv ".env" } else { Load-DotEnv ".env.example" }
if (-not $Env:API_PORT) { $Env:API_PORT = "8001" }
Write-Host "[OK] Run API on :$($Env:API_PORT)" -ForegroundColor Green
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $Env:API_PORT
exit 0
} catch {
Write-Host "[ERR] $($_.Exception.Message)" -ForegroundColor Red
exit 10
}
