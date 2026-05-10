import subprocess
import time
import os
import sys
import webview
import ctypes
import socket

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def main():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    ui_dir = os.path.join(os.getcwd(), "forge-vault-terminal-main", "forge-vault-terminal-main")
    dist_dir = os.path.join(ui_dir, "dist")

    # Check if UI is built
    if not os.path.exists(dist_dir):
        print("[!] ERROR: UI build folder ('dist') not found.")
        print(f"[!] Please run: cd {ui_dir} && npm install && npm run build")
        input("Press Enter to exit...")
        sys.exit()

    print("[*] Starting Retail OS Forge Engine (Port 8000)...")
    # 1. Start the API Server (Headless Engine)
    api_proc = subprocess.Popen(
        [sys.executable, "api_server.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    print("[*] Starting Modern UI Server (Port 4173)...")
    # 2. Start the UI Server (Vite Preview)
    ui_proc = subprocess.Popen(
        ["npm", "run", "preview"],
        cwd=ui_dir,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    # 3. Wait for servers to be ready (Polling)
    print("[*] Waiting for services to initialize...")
    timeout = 30
    start_time = time.time()
    api_ready = False
    ui_ready = False

    while time.time() - start_time < timeout:
        if not api_ready and is_port_open(8000):
            api_ready = True
            print("[+] Engine ready.")
        if not ui_ready and is_port_open(4173):
            ui_ready = True
            print("[+] UI Server ready.")
        
        if api_ready and ui_ready:
            break
        time.sleep(1)

    if not api_ready or not ui_ready:
        print("[!] ERROR: One or more services failed to start.")
        print(f"    Engine (8000): {'Ready' if api_ready else 'FAILED'}")
        print(f"    UI Server (4173): {'Ready' if ui_ready else 'FAILED'}")
        print("[!] Ensure ports 8000 and 4173 are not in use.")
        api_proc.terminate()
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(ui_proc.pid)], capture_output=True)
        input("Press Enter to exit...")
        sys.exit()

    # 4. Launch WebView
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
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(ui_proc.pid)], capture_output=True)
        api_proc.wait()

if __name__ == "__main__":
    main()
