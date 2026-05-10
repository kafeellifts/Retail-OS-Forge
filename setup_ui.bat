@echo off
echo [*] Setting up Modern UI...
set UI_PATH=forge-vault-terminal-main\forge-vault-terminal-main

if not exist "%UI_PATH%\package.json" (
    echo [!] ERROR: Could not find UI folder at %UI_PATH%
    echo [!] Please ensure you are running this from the root of the Retail-OS-Forge repository.
    pause
    exit /b
)

echo [*] Navigating to %UI_PATH%...
pushd "%UI_PATH%"

echo [*] Installing Node dependencies...
call npm install

echo [*] Building UI assets...
call npm run build

popd
echo [*] UI Setup Complete! You can now run 'python main.py'
pause
