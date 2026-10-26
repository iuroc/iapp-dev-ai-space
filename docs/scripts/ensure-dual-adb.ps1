# Keep the two LDPlayer installs on distinct host adb ports.
#
# Why: both installs run their only instance as index=0, so each VM adds the same
# NAT rule "adb,tcp,,5555,,5555" when it boots. Two listeners on host 0.0.0.0:5555
# mean adb may silently attach to the wrong Android version.
#
# Mapping (target state):
#   LDPlayer9  (Android 9  / API 28) -> host 5555  (emulator-5554 keeps working)
#   LDPlayer14 (Android 14 / API 34) -> host 5557  (adb connect 127.0.0.1:5557)
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File ensure-dual-adb.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File ensure-dual-adb.ps1 -Watch
#
# LDPlayer rewrites the VM config at every launch, so the rule has to be re-applied
# after each emulator start. -Watch polls and fixes it automatically.

param(
    [switch]$Watch,
    [int]$IntervalSeconds = 5
)

$ErrorActionPreference = 'SilentlyContinue'

$vbox = 'C:\Program Files\ldplayer9box\VBoxManage.exe'
$adb  = 'E:\Program Files\platform-tools\adb.exe'

$targets = @(
    [pscustomobject]@{ Name = 'LDPlayer9-Android9';  Uuid = '20160302-aaaa-aaaa-012e-000000000000'; Port = 5555 },
    [pscustomobject]@{ Name = 'LDPlayer14-Android14'; Uuid = '20160302-aaaa-aaaa-7046-000000000000'; Port = 5557 }
)

function Sync-One($t) {
    $info = & $vbox showvminfo $t.Uuid --machinereadable 2>$null
    if (-not $info) { return $false }
    if (-not ($info | Where-Object { $_ -match '^VMState="running"' })) { return $false }

    $want  = "adb,tcp,,$($t.Port),,5555"
    $rules = @($info | Where-Object { $_ -match '^Forwarding\(\d+\)="adb,' })

    if (($rules.Count -eq 1) -and ($rules[0] -match ('=' + [regex]::Escape('"' + $want + '"') + '$'))) {
        return $false
    }

    foreach ($r in $rules) {
        # line looks like: Forwarding(0)="adb,tcp,,5555,,5555"
        $name = ($r -split '"')[1].Split(',')[0]
        & $vbox controlvm $t.Uuid natpf1 delete $name 2>$null | Out-Null
        Start-Sleep -Milliseconds 300
    }
    & $vbox controlvm $t.Uuid natpf1 $want 2>$null | Out-Null
    Write-Host ("[{0}] {1}: adb -> {2}" -f (Get-Date -Format 'HH:mm:ss'), $t.Name, $want)
    return $true
}

function Sync-All {
    $changed = $false
    foreach ($t in $targets) {
        if (Sync-One $t) { $changed = $true }
    }
    if ($changed) {
        # stale transports still point at the old NAT mapping
        & $adb kill-server  2>$null | Out-Null
        Start-Sleep -Seconds 1
        & $adb start-server 2>$null | Out-Null
        Start-Sleep -Seconds 1
        & $adb connect 127.0.0.1:5557 2>$null | Out-Null
        Write-Host 'adb restarted: Android 9 = emulator-5554, Android 14 = 127.0.0.1:5557'
    }
    return $changed
}

if (-not (Test-Path $vbox)) { Write-Error "VBoxManage not found: $vbox"; exit 1 }

Sync-All | Out-Null

if ($Watch) {
    while ($true) {
        Start-Sleep -Seconds $IntervalSeconds
        Sync-All | Out-Null
    }
}
