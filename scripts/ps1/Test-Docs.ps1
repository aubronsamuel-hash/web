$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Fail($code, $msg){ Write-Host "[FAIL] $msg" -ForegroundColor Red; exit $code }
function Ok($msg){ Write-Host "[OK] $msg" -ForegroundColor Green }

# EXIT_CODES

# 0 OK; 1 USAGE_INVALIDE; 2 PREREQUIS_MANQUANTS; 10 ERREUR_INTERNE.

try {
$required = @(
"README.md",
"docs\ARCHITECTURE.md",
"docs\ROADMAP.md",
"docs\RELEASE.md",
"docs\CONTRIBUTING.md",
"docs\OPS_WINDOWS.md",
"docs\OPS_LINUX.md",
"docs\SECURITY.md",
"docs\CODE_OF_CONDUCT.md",
".env.example",
".github\pull_request_template.md",
".github\ISSUE_TEMPLATE\bug_report.md",
".github\ISSUE_TEMPLATE\feature_request.md"
)

foreach($f in $required){
    if(-not (Test-Path $f)){ Fail 2 "Fichier manquant: $f" } else { Ok "Present: $f" }
    $bytes = [System.IO.File]::ReadAllBytes($f)
    foreach($b in $bytes){ if($b -gt 127){ Fail 1 "Non-ASCII detecte dans $f" } }
    $lines = Get-Content $f -Encoding ASCII
    $i=0
    foreach($line in $lines){ $i++; if($line.Length -gt 120){ Fail 1 "Ligne >120 chars: $f:$i" } }
}

Ok "Verification docs OK."
exit 0

}
catch {
Fail 10 $_.Exception.Message
}
