# ui.py

import customtkinter as ctk
import threading
from config import DEBLOAT_COMMANDS, OPTIMIZATION_COMMANDS, POS_SOFTWARE
from engine import ProvisioningEngine

class RetailOSForgeUI(ctk.CTk):
    """
    Main UI Class for Retail OS Forge using customtkinter.
    """
    def __init__(self):
        super().__init__()

        self.title("Retail OS Forge")
        self.geometry("650x700")
        self.resizable(False, False)
        
        # Configure grid for main window
        self.grid_columnconfigure(0, weight=1)

        # Main Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="RETAIL OS FORGE", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- Debloat Level Selection ---
        self.debloat_frame = ctk.CTkFrame(self)
        self.debloat_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.debloat_label = ctk.CTkLabel(
            self.debloat_frame, 
            text="Debloat Level:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.debloat_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.debloat_var = ctk.StringVar(value="None")
        
        self.radio_none = ctk.CTkRadioButton(self.debloat_frame, text="None", variable=self.debloat_var, value="None")
        self.radio_none.grid(row=0, column=1, padx=10, pady=15)
        
        self.radio_basic = ctk.CTkRadioButton(self.debloat_frame, text="Basic", variable=self.debloat_var, value="Basic")
        self.radio_basic.grid(row=0, column=2, padx=10, pady=15)
        
        self.radio_aggressive = ctk.CTkRadioButton(self.debloat_frame, text="Aggressive", variable=self.debloat_var, value="Aggressive")
        self.radio_aggressive.grid(row=0, column=3, padx=10, pady=15)

        # --- System Optimizations ---
        self.opt_frame = ctk.CTkFrame(self)
        self.opt_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.opt_var = ctk.BooleanVar(value=False)
        self.opt_checkbox = ctk.CTkCheckBox(
            self.opt_frame, 
            text="Apply Advanced System Optimizations", 
            variable=self.opt_var,
            font=ctk.CTkFont(size=14)
        )
        self.opt_checkbox.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        # --- POS Software Selection ---
        self.pos_frame = ctk.CTkFrame(self)
        self.pos_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.pos_label = ctk.CTkLabel(
            self.pos_frame, 
            text="Select POS Software:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.pos_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.pos_var = ctk.StringVar(value="None")
        pos_options = list(POS_SOFTWARE.keys())
        
        self.pos_dropdown = ctk.CTkOptionMenu(
            self.pos_frame, 
            variable=self.pos_var, 
            values=pos_options,
            width=200
        )
        self.pos_dropdown.grid(row=0, column=1, padx=15, pady=15, sticky="w")

        # --- Terms & Conditions ---
        self.tc_var = ctk.BooleanVar(value=False)
        self.tc_checkbox = ctk.CTkCheckBox(
            self, 
            text="I agree to the Terms & Conditions and understand these changes.", 
            variable=self.tc_var, 
            command=self.toggle_forge_button
        )
        self.tc_checkbox.grid(row=4, column=0, padx=20, pady=(20, 10))

        # --- FORGE Button ---
        self.forge_button = ctk.CTkButton(
            self, 
            text="FORGE", 
            font=ctk.CTkFont(size=20, weight="bold"), 
            height=50, 
            command=self.start_provisioning, 
            state="disabled",
            fg_color="#8B0000",
            hover_color="#5C0000"
        )
        self.forge_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # --- Log Output Box ---
        self.log_textbox = ctk.CTkTextbox(
            self, 
            state="disabled", 
            height=180,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.log_textbox.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.grid_rowconfigure(6, weight=1)

    def toggle_forge_button(self):
        """Enable or disable the Forge button based on T&C checkbox."""
        if self.tc_var.get():
            self.forge_button.configure(state="normal")
        else:
            self.forge_button.configure(state="disabled")

    def log_update(self, message):
        """Thread-safe call to update the UI log box."""
        self.after(0, self._append_log, message)

    def _append_log(self, message):
        """Helper to safely insert string into read-only textbox."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def start_provisioning(self):
        """Called when FORGE button is clicked. Initiates background thread."""
        # Disable interactions while running
        self.forge_button.configure(state="disabled")
        self.tc_checkbox.configure(state="disabled")
        
        # Clear logs
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.configure(state="disabled")

        # Gather inputs
        debloat_level = self.debloat_var.get()
        debloat_cmds = DEBLOAT_COMMANDS.get(debloat_level, [])
        
        apply_opt = self.opt_var.get()
        opt_cmds = OPTIMIZATION_COMMANDS
        
        pos_selection = self.pos_var.get()
        pos_cmds = POS_SOFTWARE.get(pos_selection, [])

        # Initialize the engine
        engine = ProvisioningEngine(callback=self.log_update)
        
        # Spawn daemon thread to avoid blocking the main UI thread
        thread = threading.Thread(
            target=self._run_engine_thread, 
            args=(engine, debloat_cmds, apply_opt, opt_cmds, pos_cmds)
        )
        thread.daemon = True
        thread.start()

    def _run_engine_thread(self, engine, debloat_cmds, apply_opt, opt_cmds, pos_cmds):
        """Thread worker to run the provisioning and re-enable UI."""
        engine.run_provisioning(debloat_cmds, apply_opt, opt_cmds, pos_cmds)
        
        # Re-enable the UI components safely via main thread
        self.after(0, self._on_provisioning_complete)

    def _on_provisioning_complete(self):
        """Restore UI state post-provisioning."""
        self.tc_checkbox.configure(state="normal")
        if self.tc_var.get():
            self.forge_button.configure(state="normal")
