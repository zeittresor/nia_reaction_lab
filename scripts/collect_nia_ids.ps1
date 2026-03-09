# Plug in the NIA first, then run this script in PowerShell.
$devices = Get-PnpDevice | Where-Object {
    $_.InstanceId -like 'USB\VID_1234&PID_0000*' -or $_.FriendlyName -like '*NIA*'
}

if (-not $devices) {
    Write-Host 'No matching NIA device found.' -ForegroundColor Yellow
    exit 1
}

foreach ($dev in $devices) {
    Write-Host '----------------------------------------' -ForegroundColor DarkGray
    Write-Host "Friendly Name : $($dev.FriendlyName)"
    Write-Host "Status        : $($dev.Status)"
    Write-Host "Class         : $($dev.Class)"
    Write-Host "Instance ID   : $($dev.InstanceId)"
    try {
        Get-PnpDeviceProperty -InstanceId $dev.InstanceId -KeyName 'DEVPKEY_Device_HardwareIds' |
            Format-List
    } catch {
        Write-Host 'Could not read DEVPKEY_Device_HardwareIds.' -ForegroundColor Yellow
    }
}
