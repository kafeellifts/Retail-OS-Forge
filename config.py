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
    "Marg": [
        "Write-Host 'Downloading Marg POS...'",
        "Start-Sleep -Seconds 2",
        "Write-Host 'Installing Marg POS silently...'",
        "Write-Host 'Marg POS Installation Complete.'"
    ],
    "TallyPrime": [
        "Write-Host 'Downloading TallyPrime...'",
        "Start-Sleep -Seconds 2",
        "Write-Host 'Installing TallyPrime silently...'",
        "Write-Host 'TallyPrime Installation Complete.'"
    ],
    "Vyapar": [
        "Write-Host 'Downloading Vyapar...'",
        "Start-Sleep -Seconds 2",
        "Write-Host 'Installing Vyapar silently...'",
        "Write-Host 'Vyapar Installation Complete.'"
    ]
}
