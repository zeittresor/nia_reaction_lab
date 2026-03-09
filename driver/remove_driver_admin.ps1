# Requires: elevated PowerShell
$matches = pnputil /enum-drivers | Select-String -Pattern 'OCZ NIA \(Experimental WinUSB Binding\)' -Context 0,4
if (-not $matches) {
    Write-Host 'No matching installed OCZ NIA experimental package found.' -ForegroundColor Yellow
    exit 0
}

$published = @()
foreach ($m in $matches) {
    foreach ($line in $m.Context.PostContext) {
        if ($line -match 'Published Name\s*:\s*(oem\d+\.inf)') {
            $published += $Matches[1]
        }
    }
}

$published = $published | Sort-Object -Unique
foreach ($name in $published) {
    Write-Host "Removing $name" -ForegroundColor Cyan
    pnputil /delete-driver $name /uninstall /force
}
