# main.py

import ctypes
import sys
import os
import customtkinter as ctk
from ui import RetailOSForgeUI

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

    """
    Entry point for the Retail OS Forge application.
    """
    # Set the overall appearance and color theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Initialize and run the application
    app = RetailOSForgeUI()
    app.mainloop()

if __name__ == "__main__":
    main()
