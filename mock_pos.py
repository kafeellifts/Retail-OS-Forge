import sys
import os
import shutil
import subprocess

exe_name = os.path.basename(sys.executable)
if exe_name.lower().endswith('.exe'):
    app_name = exe_name[:-4].replace('_', ' ').replace('Setup', '')
else:
    app_name = "Point of Sale Terminal"

def install_silently():
    # Simulate a real installer
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if not local_app_data:
        sys.exit(1)
        
    install_dir = os.path.join(local_app_data, 'RetailOS', 'POS')
    os.makedirs(install_dir, exist_ok=True)
    
    target_exe = os.path.join(install_dir, f"{app_name}.exe")
    
    # Copy ourselves to the target directory
    shutil.copy2(sys.executable, target_exe)
    
    # Create desktop shortcut using PowerShell
    ps_cmd = f"""
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\\Desktop\\{app_name}.lnk")
    $Shortcut.TargetPath = "{target_exe}"
    $Shortcut.Save()
    """
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
    sys.exit(0)

if "/VERYSILENT" in sys.argv or "/S" in sys.argv:
    install_silently()

import customtkinter as ctk

# Setup the application window
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title(f"{app_name} - Retail Dashboard")
app.geometry("800x500")

# Header
header = ctk.CTkFrame(app, corner_radius=0, fg_color="#1f232a")
header.pack(fill="x", pady=0)
title_label = ctk.CTkLabel(header, text=f"Welcome to {app_name}", font=("Inter", 24, "bold"), text_color="#00ffcc")
title_label.pack(pady=20)

# Main content
content = ctk.CTkFrame(app, fg_color="transparent")
content.pack(expand=True, fill="both", padx=20, pady=20)

# Sidebar (Navigation)
sidebar = ctk.CTkFrame(content, width=200, corner_radius=10)
sidebar.pack(side="left", fill="y", padx=(0, 20))

nav_items = ["Dashboard", "Inventory", "Sales", "Reports", "Settings"]
for item in nav_items:
    btn = ctk.CTkButton(sidebar, text=item, fg_color="transparent", text_color="white", hover_color="#2b303b", anchor="w", font=("Inter", 14))
    btn.pack(fill="x", padx=10, pady=5)

# Main Dashboard Area
dashboard = ctk.CTkFrame(content, corner_radius=10)
dashboard.pack(side="right", expand=True, fill="both")

info_label = ctk.CTkLabel(dashboard, text="System Ready.", font=("Inter", 18))
info_label.pack(pady=(20, 10))

desc_label = ctk.CTkLabel(dashboard, text=f"This is a placeholder application demonstrating that\n{app_name} was successfully installed by Retail OS Forge.", font=("Inter", 14), text_color="gray")
desc_label.pack(pady=10)

stats_frame = ctk.CTkFrame(dashboard, fg_color="transparent")
stats_frame.pack(fill="x", pady=20, padx=20)

def create_stat_card(parent, title, value):
    card = ctk.CTkFrame(parent, corner_radius=8, fg_color="#2b303b")
    card.pack(side="left", expand=True, fill="both", padx=10)
    ctk.CTkLabel(card, text=title, font=("Inter", 12), text_color="gray").pack(pady=(10, 0))
    ctk.CTkLabel(card, text=value, font=("Inter", 20, "bold"), text_color="#00ffcc").pack(pady=(5, 10))

create_stat_card(stats_frame, "Today's Sales", "$1,245.00")
create_stat_card(stats_frame, "Active Orders", "14")
create_stat_card(stats_frame, "Low Stock Items", "3")

if __name__ == "__main__":
    app.mainloop()
