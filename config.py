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
        "Write-Host 'Downloading Marg ERP 9+...'",
        "Invoke-WebRequest -Uri 'https://margcompusoft.com/download/MargSetup.exe' -OutFile \"$env:TEMP\\MargSetup.exe\" -UseBasicParsing -ErrorAction SilentlyContinue",
        "Write-Host 'Installing Marg ERP silently...'",
        "Start-Process -FilePath \"$env:TEMP\\MargSetup.exe\" -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART' -Wait -NoNewWindow -ErrorAction SilentlyContinue",
        "Remove-Item -Path \"$env:TEMP\\MargSetup.exe\" -Force -ErrorAction SilentlyContinue",
        "Write-Host 'Marg ERP Installation Complete.'"
    ],
    "TallyPrime": [
        "Write-Host 'Downloading TallyPrime...'",
        "Invoke-WebRequest -Uri 'https://mirror.tallysolutions.com/Downloads/TallyPrime/setup.exe' -OutFile \"$env:TEMP\\TallySetup.exe\" -UseBasicParsing -ErrorAction SilentlyContinue",
        "Write-Host 'Installing TallyPrime silently...'",
        "Start-Process -FilePath \"$env:TEMP\\TallySetup.exe\" -ArgumentList '/s' -Wait -NoNewWindow -ErrorAction SilentlyContinue",
        "Remove-Item -Path \"$env:TEMP\\TallySetup.exe\" -Force -ErrorAction SilentlyContinue",
        "Write-Host 'TallyPrime Installation Complete.'"
    ],
    "Busy Accounting": [
        "Write-Host 'Downloading Busy Accounting...'",
        "Invoke-WebRequest -Uri 'https://busy.in/download/busy21.exe' -OutFile \"$env:TEMP\\BusySetup.exe\" -UseBasicParsing -ErrorAction SilentlyContinue",
        "Write-Host 'Installing Busy Accounting silently...'",
        "Start-Process -FilePath \"$env:TEMP\\BusySetup.exe\" -ArgumentList '/S', '/v/qn' -Wait -NoNewWindow -ErrorAction SilentlyContinue",
        "Remove-Item -Path \"$env:TEMP\\BusySetup.exe\" -Force -ErrorAction SilentlyContinue",
        "Write-Host 'Busy Accounting Installation Complete.'"
    ],
    "Vyapar": [
        "Write-Host 'Downloading Vyapar...'",
        "Invoke-WebRequest -Uri 'https://static.vyaparapp.in/installers/Vyapar-setup.exe' -OutFile \"$env:TEMP\\VyaparSetup.exe\" -UseBasicParsing -ErrorAction SilentlyContinue",
        "Write-Host 'Installing Vyapar silently...'",
        "Start-Process -FilePath \"$env:TEMP\\VyaparSetup.exe\" -ArgumentList '/S' -Wait -NoNewWindow -ErrorAction SilentlyContinue",
        "Remove-Item -Path \"$env:TEMP\\VyaparSetup.exe\" -Force -ErrorAction SilentlyContinue",
        "Write-Host 'Vyapar Installation Complete.'"
    ],
    "Zoho Inventory": [
        "Write-Host 'Creating Desktop Shortcut for Zoho Inventory Web...'",
        "$WshShell = New-Object -comObject WScript.Shell",
        "$Shortcut = $WshShell.CreateShortcut(\"$env:USERPROFILE\\Desktop\\Zoho Inventory.lnk\")",
        "$Shortcut.TargetPath = 'msedge.exe'",
        "$Shortcut.Arguments = 'https://inventory.zoho.com'",
        "$Shortcut.Save()",
        "Write-Host 'Zoho Inventory Setup Complete.'"
    ],
    "Hitech BillSoft": [
        "Write-Host 'Downloading Hitech BillSoft...'",
        "Invoke-WebRequest -Uri 'https://billingsoftware.in/download/HitechBillSoft.exe' -OutFile \"$env:TEMP\\HitechSetup.exe\" -UseBasicParsing -ErrorAction SilentlyContinue",
        "Write-Host 'Installing Hitech BillSoft silently...'",
        "Start-Process -FilePath \"$env:TEMP\\HitechSetup.exe\" -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES' -Wait -NoNewWindow -ErrorAction SilentlyContinue",
        "Remove-Item -Path \"$env:TEMP\\HitechSetup.exe\" -Force -ErrorAction SilentlyContinue",
        "Write-Host 'Hitech BillSoft Installation Complete.'"
    ]
}
