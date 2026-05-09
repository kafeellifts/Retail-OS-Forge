# main.py

import customtkinter as ctk
from ui import RetailOSForgeUI

def main():
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
