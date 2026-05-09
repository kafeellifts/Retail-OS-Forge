# engine.py

import subprocess
import time

class ProvisioningEngine:
    """
    Executes Windows PowerShell commands sequentially and safely.
    Sends output back to the UI via a callback mechanism.
    """
    def __init__(self, callback):
        self.callback = callback

    def execute_commands(self, commands):
        for cmd in commands:
            self.callback(f"> {cmd}\n")
            try:
                # Execute command without spawning a visible console window
                process = subprocess.run(
                    ["powershell", "-Command", cmd],
                    shell=True,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if process.stdout:
                    self.callback(f"{process.stdout}\n")
                if process.stderr:
                    self.callback(f"ERROR: {process.stderr}\n")
                    
            except Exception as e:
                self.callback(f"EXCEPTION: {str(e)}\n")
            
            # Small delay to ensure logs aren't processed completely instantly
            time.sleep(0.1)

    def run_provisioning(self, debloat_cmds, apply_opt, opt_cmds, pos_cmds):
        self.callback("=== Starting Retail OS Forge Provisioning ===\n")
        
        if debloat_cmds:
            self.callback("\n--- Executing Debloat ---\n")
            self.execute_commands(debloat_cmds)
            
        if apply_opt and opt_cmds:
            self.callback("\n--- Executing Optimizations ---\n")
            self.execute_commands(opt_cmds)
            
        if pos_cmds:
            self.callback("\n--- Installing POS Software ---\n")
            self.execute_commands(pos_cmds)
            
        self.callback("\n=== Provisioning Complete! ===\n")
