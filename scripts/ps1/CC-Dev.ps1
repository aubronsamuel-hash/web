[CmdletBinding()]
param(
    [switch]$Reinstall
)
$ErrorActionPreference = 'Stop'

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error 'Python introuvable.'
    exit 2
}

if ($Reinstall) {
    & $python.Source -m pip uninstall -y cc > $null 2>&1
}

$cliPath = Resolve-Path "$PSScriptRoot/../../cli"
& $python.Source -m pip install -e $cliPath > $null

if (-not $IsWindows) {
    $wrapper = '/usr/local/bin/cc'
    $content = @'
#!/usr/bin/env bash
PYTHON -m cc.cli "$@"
'@
    $content = $content -replace 'PYTHON', $python.Source
    Set-Content -Path $wrapper -Value $content
    chmod +x $wrapper 2>$null
}

Write-Host '[OK] Environnement installe.'
cc --version
