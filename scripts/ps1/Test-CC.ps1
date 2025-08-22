$ErrorActionPreference = 'Stop'

function Run($cmd, $expected = 0) {
    Invoke-Expression $cmd
    $code = $LASTEXITCODE
    if ($code -ne $expected) {
        Write-Error "Commande '$cmd' sortie $code attendue $expected"
        exit $code
    }
}

Run 'cc --version'
Run 'cc env'
Run 'cc env --json'

cc check
$check = $LASTEXITCODE
if ($check -ne 0 -and $check -ne 2) {
    Write-Error "cc check code $check"
    exit $check
}

$py = @'
import socket, time
s = socket.socket()
s.bind(('127.0.0.1', 8765))
s.listen(1)
conn, addr = s.accept()
time.sleep(5)
'@
$job = Start-Job -ScriptBlock { param($s) python -c $s } -ArgumentList $py
Start-Sleep -Milliseconds 200
$env:API_BASE = 'http://127.0.0.1:8765'
cc ping --timeout 1
$code = $LASTEXITCODE
Stop-Job $job | Out-Null
if ($code -ne 3) {
    Write-Error "cc ping code $code"
    exit $code
}

Write-Host '[OK] Tests passes.'
