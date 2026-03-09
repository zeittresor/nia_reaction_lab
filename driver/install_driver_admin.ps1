# Requires: elevated PowerShell
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$inf = Join-Path $here 'ocz_nia_winusb.inf'

Write-Host "Adding driver package: $inf" -ForegroundColor Cyan
pnputil /add-driver $inf /install
Write-Host "Done. If Windows blocks the package, the INF still needs a trusted signature." -ForegroundColor Yellow
