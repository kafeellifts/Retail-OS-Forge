import subprocess
import time
import os
import sys
import webview
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("[*] Starting Retail OS Forge Engine...")
    # 1. Start the API Server (Headless Engine)
    # We use uvicorn directly or run api_server.py
    api_proc = subprocess.Popen(
        [sys.executable, "api_server.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    print("[*] Launching Modern UI Terminal...")
    # 2. Start the UI Server (Vite Preview)
    # The UI is located in the nested forge-vault-terminal-main folder
    ui_dir = os.path.join(os.getcwd(), "forge-vault-terminal-main", "forge-vault-terminal-main")
    
    # Ensure dependencies and build exist (we've handled this, but for the teammate...)
    # For now, we assume 'npm run preview' is ready.
    ui_proc = subprocess.Popen(
        ["npm", "run", "preview"],
        cwd=ui_dir,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    # 3. Wait for UI to be ready
    time.sleep(5)

    # 4. Launch WebView pointing to the Vite preview port
    window = webview.create_window(
        "Retail OS Forge",
        "http://localhost:4173",
        width=1100,
        height=900,
        resizable=True,
        background_color="#000000"
    )
    
    try:
        webview.start(debug=False)
    finally:
        # Cleanup background processes on exit
        print("[*] Shutting down services...")
        api_proc.terminate()
        # Taskkill might be needed for npm/node processes on Windows
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(ui_proc.pid)], capture_output=True)
        api_proc.wait()

if __name__ == "__main__":
    main()
