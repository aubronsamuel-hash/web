Param(
[switch]$Force
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Ok($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Write-Err($m){ Write-Host "[ERR] $m" -ForegroundColor Red }

try {
$root = Split-Path -Parent $PSCommandPath
$repoRoot = Resolve-Path (Join-Path $root "....")
Set-Location $repoRoot

$files = @(
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

foreach($f in $files){
    $dir = Split-Path $f -Parent
    if($dir -and -not (Test-Path $dir)){ New-Item -ItemType Directory -Path $dir | Out-Null }

    if((Test-Path $f) -and -not $Force){
        Write-Ok "$f existe, passer (--Force pour ecraser)."
        continue
    }

    switch ($f){
        "README.md" { @"
# Coulisses Crew

Projet SaaS de planification pour intermittents. Voir docs/.
"@ | Out-File -FilePath $f -Encoding ASCII -NoNewline }
        "docs\ARCHITECTURE.md" { @"
# Architecture

Voir README principal pour le resume.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\ROADMAP.md" { @"
# Roadmap

Voir gates par etapes.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\RELEASE.md" { @"
# Release

Procedure de versionnage.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\CONTRIBUTING.md" { @"
# Contributing

ASCII, Windows-first, PR <= 300 lignes.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\OPS_WINDOWS.md" { @"
# OPS Windows

Scripts PowerShell dans scripts/ps1.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\OPS_LINUX.md" { @"
# OPS Linux

Utiliser pwsh si besoin. Scripts officiels .ps1.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\SECURITY.md" { @"
# Securite

Pas de secrets commit.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        "docs\CODE_OF_CONDUCT.md" { @"
# Code of Conduct

Respect et collaboration.
"@ | Out-File $f -Encoding ASCII -NoNewline }
        ".env.example" { @"
APP_NAME=CoulissesCrew
ENV=dev
LOG_LEVEL=INFO
"@ | Out-File $f -Encoding ASCII -NoNewline }
        ".github\pull_request_template.md" { @"
## Objet

Decrire le changement (court).
"@ | Out-File $f -Encoding ASCII -NoNewline }
        ".github\ISSUE_TEMPLATE\bug_report.md" { @"
name: Bug report
description: Signaler un bug
title: ""[BUG] Titre concis""
labels: [""bug""]
"@ | Out-File $f -Encoding ASCII -NoNewline }
        ".github\ISSUE_TEMPLATE\feature_request.md" { @"
name: Feature request
description: Demande de fonctionnalite
title: ""[FEAT] Titre concis""
labels: [""enhancement""]
"@ | Out-File $f -Encoding ASCII -NoNewline }
    }
    Write-Ok "Genere: $f"
}

Write-Ok "Docs initiales generees."
exit 0

}
catch {
Write-Err $_.Exception.Message
exit 10
}
