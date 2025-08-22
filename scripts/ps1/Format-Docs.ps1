$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Trim-File($path){
$lines = Get-Content $path -Encoding ASCII
$lines = $lines | ForEach-Object { $_.TrimEnd() }
$out = [string]::Join([Environment]::NewLine, $lines)
$out | Out-File -FilePath $path -Encoding ASCII -NoNewline
}

$targets = @(
"README.md",
"docs\*.md",
".github\*\*\*.md",
".env.example"
)

foreach($t in $targets){
Get-ChildItem -Path $t -File -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
Trim-File $_.FullName
Write-Host "[OK] Formate: $($_.FullName)" -ForegroundColor Green
}
}
exit 0
