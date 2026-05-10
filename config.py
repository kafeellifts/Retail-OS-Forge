# config.py

"""
Configuration file for Retail OS Forge.
Stores provisioning commands and definitions for debloat, optimizations, and POS software.
"""

DEBLOAT_COMMANDS = {
    "Basic": [
        "Write-Host 'Starting Basic Debloat...'",
        "Get-AppxPackage *bing* | Remove-AppxPackage -ErrorAction SilentlyContinue",
        "Get-AppxPackage *zune* | Remove-AppxPackage -ErrorAction SilentlyContinue",
        "Write-Host 'Basic Debloat Complete.'"
    ],
    "Aggressive": [
        "Write-Host 'Starting Aggressive Debloat...'",
        "Get-AppxPackage -AllUsers | where-object {$_.name -notlike '*store*'} | Remove-AppxPackage -ErrorAction SilentlyContinue",
        "Write-Host 'Aggressive Debloat Complete.'"
    ]
}

OPTIMIZATION_COMMANDS = [
    "Write-Host 'Applying System Optimizations...'",
    "Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Session Manager\\Memory Management' -Name 'ClearPageFileAtShutdown' -Value 1",
    "Write-Host 'System Optimizations Applied.'"
]

POS_SOFTWARE = {
    "None": [],
    "Marg ERP 9+": [
        "Write-Host 'Checking for Marg ERP installer...'",
        "$installer = \"$PWD\installers\MargSetup.exe\"",
        "if (Test-Path $installer) {",
        "    Write-Host 'Executing local installer for Marg ERP...'",
        "    Start-Process -FilePath $installer -ArgumentList '/VERYSILENT' -Wait -NoNewWindow",
        "    Write-Host 'Marg ERP Setup Complete.'",
        "} else {",
        "    Write-Host 'MargSetup.exe not found in installers/ folder! Launching download page...'",
        "    Start-Process 'https://margcompusoft.com/download/'",
        "}"
    ],
    "TallyPrime": [
        "Write-Host 'Checking for TallyPrime installer...'",
        "$installer = \"$PWD\installers\TallyPrimeSetup.exe\"",
        "if (Test-Path $installer) {",
        "    Write-Host 'Executing local installer for TallyPrime...'",
        "    Start-Process -FilePath $installer -ArgumentList '/VERYSILENT' -Wait -NoNewWindow",
        "    Write-Host 'TallyPrime Setup Complete.'",
        "} else {",
        "    Write-Host 'TallyPrimeSetup.exe not found in installers/ folder! Launching download page...'",
        "    Start-Process 'https://tallysolutions.com/download/'",
        "}"
    ],
    "Busy Accounting": [
        "Write-Host 'Checking for Busy Accounting installer...'",
        "$installer = \"$PWD\installers\BusySetup.exe\"",
        "if (Test-Path $installer) {",
        "    Write-Host 'Executing local installer for Busy...'",
        "    Start-Process -FilePath $installer -ArgumentList '/VERYSILENT' -Wait -NoNewWindow",
        "    Write-Host 'Busy Setup Complete.'",
        "} else {",
        "    Write-Host 'BusySetup.exe not found in installers/ folder! Launching download page...'",
        "    Start-Process 'https://busy.in/bdownload/busy.exe'",
        "}"
    ],
    "Vyapar": [
        "Write-Host 'Checking for Vyapar installer...'",
        "$installer = \"$PWD\installers\VyaparSetup.exe\"",
        "if (Test-Path $installer) {",
        "    Write-Host 'Executing local installer for Vyapar...'",
        "    Start-Process -FilePath $installer -ArgumentList '/VERYSILENT' -Wait -NoNewWindow",
        "    Write-Host 'Vyapar Setup Complete.'",
        "} else {",
        "    Write-Host 'VyaparSetup.exe not found in installers/ folder! Launching download page...'",
        "    Start-Process 'https://vyaparapp.in'",
        "}"
    ],
    "Zoho Inventory": [
        "Write-Host 'Checking for Zoho Inventory installer...'",
        "$installer = \"$PWD\installers\ZohoSetup.exe\"",
        "if (Test-Path $installer) {",
        "    Write-Host 'Executing local installer for Zoho...'",
        "    Start-Process -FilePath $installer -ArgumentList '/VERYSILENT' -Wait -NoNewWindow",
        "    Write-Host 'Zoho Setup Complete.'",
        "} else {",
        "    Write-Host 'ZohoSetup.exe not found in installers/ folder! Launching download page...'",
        "    Start-Process 'https://inventory.zoho.com'",
        "}"
    ],
    "Hitech BillSoft": [
        "Write-Host 'Checking for Hitech BillSoft installer...'",
        "$installer = \"$PWD\installers\HitechSetup.exe\"",
        "if (Test-Path $installer) {",
        "    Write-Host 'Executing local installer for Hitech...'",
        "    Start-Process -FilePath $installer -ArgumentList '/VERYSILENT' -Wait -NoNewWindow",
        "    Write-Host 'Hitech Setup Complete.'",
        "} else {",
        "    Write-Host 'HitechSetup.exe not found in installers/ folder! Launching download page...'",
        "    Start-Process 'https://billingsoftware.in'",
        "}"
    ]
}