Param(
    [int]$Count = 50
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
. ..venv\Scripts\Activate.ps1

# Login admin

$token = (Invoke-RestMethod -Method Post -Uri "http://localhost:8001/auth/token" `
  -Body @{username=$Env:ADMIN_EMAIL;password=$Env:ADMIN_PASSWORD} `
  -ContentType "application/x-www-form-urlencoded").access_token

for ($i=0; $i -lt $Count; $i++){
    try {
        Invoke-RestMethod -Method Post -Uri "http://localhost:8001/users" `
            -Headers @{Authorization="Bearer $token"} `
            -Body (@{email="user$($i)@ex.com"} | ConvertTo-Json) `
            -ContentType "application/json" | Out-Null
    } catch { }
}
Write-Host "[OK] Seed $Count users." -ForegroundColor Green
exit 0

