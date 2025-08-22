Param(
    [int]$N = 50,
    [int]$ThresholdMs = 500
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

. ..venv\Scripts\Activate.ps1

function Percentile($arr, $p){
    $sorted = $arr | Sort-Object
    $k = [math]::Ceiling(($p/100.0) * $sorted.Count) - 1
    if ($k -lt 0) { $k = 0 }
    return $sorted[$k]
}

# Obtenir token

$token = (Invoke-RestMethod -Method Post -Uri "http://localhost:8001/auth/token" `
  -Body @{username=$Env:ADMIN_EMAIL;password=$Env:ADMIN_PASSWORD} `
  -ContentType "application/x-www-form-urlencoded").access_token

# Appels series pour simplicite (facile a parallelliser plus tard)

$times = @()
for ($i=0; $i -lt $N; $i++){
    $t0 = Get-Date
    Invoke-RestMethod -Method Get -Uri "http://localhost:8001/users?page=1&size=20" `
        -Headers @{Authorization="Bearer $token"} | Out-Null
    $dt = ((Get-Date) - $t0).TotalMilliseconds
    $times += [int][math]::Round($dt)
}
$p95 = Percentile $times 95
Write-Host ("p95={0} ms (N={1})" -f $p95, $times.Count)
if ($p95 -gt $ThresholdMs){
    Write-Host "[FAIL] p95 > $ThresholdMs ms" -ForegroundColor Red
    exit 3
}
Write-Host "[OK] p95 <= $ThresholdMs ms" -ForegroundColor Green
exit 0

