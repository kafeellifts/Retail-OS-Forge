import customtkinter as ctk
import threading
import subprocess
import time
import config

class RetailOSForge(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Retail OS Forge")
        self.geometry("750x850")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, pady=(20, 10))
        self.title_label = ctk.CTkLabel(self.header_frame, text="RETAIL OS FORGE", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack()
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Hardware Provisioning Utility", font=ctk.CTkFont(size=14))
        self.subtitle_label.pack()

        # Section 1: Debloat Level
        self.sec1_frame = ctk.CTkFrame(self)
        self.sec1_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.sec1_label = ctk.CTkLabel(self.sec1_frame, text="1. Debloat Level", font=ctk.CTkFont(weight="bold"))
        self.sec1_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.debloat_var = ctk.StringVar(value="None")
        self.rb_agg = ctk.CTkRadioButton(self.sec1_frame, text="Aggressive (Removes Xbox, Zune, Bing, Cortana, Solitaire, etc.)", variable=self.debloat_var, value="Aggressive")
        self.rb_agg.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.rb_bas = ctk.CTkRadioButton(self.sec1_frame, text="Basic (Removes Xbox and Zune only)", variable=self.debloat_var, value="Basic")
        self.rb_bas.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.rb_none = ctk.CTkRadioButton(self.sec1_frame, text="None (Skips debloat)", variable=self.debloat_var, value="None")
        self.rb_none.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="w")

        # Section 2: POS Software Selection
        self.sec2_frame = ctk.CTkFrame(self)
        self.sec2_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.sec2_label = ctk.CTkLabel(self.sec2_frame, text="2. POS Software Selection", font=ctk.CTkFont(weight="bold"))
        self.sec2_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.pos_var = ctk.StringVar(value="Marg ERP 9+")
        pos_options = [
            ("Marg ERP 9+", "Requires SQL Express & .NET"),
            ("TallyPrime", "Requires .NET 4.7"),
            ("Busy Accounting", "Best for Multi-branch"),
            ("Vyapar", "Lightweight, modern UI"),
            ("Zoho Inventory", "Cloud-synced"),
            ("Hitech BillSoft", "Offline-first"),
            ("None", "Skip POS installation")
        ]
        
        for i, (name, subtitle) in enumerate(pos_options):
            rb = ctk.CTkRadioButton(self.sec2_frame, text=f"{name} - [{subtitle}]", variable=self.pos_var, value=name)
            rb.grid(row=i+1, column=0, padx=20, pady=5, sticky="w")

        # Section 3: Optimizations
        self.sec3_frame = ctk.CTkFrame(self)
        self.sec3_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.opt_var = ctk.BooleanVar(value=False)
        self.opt_cb = ctk.CTkCheckBox(self.sec3_frame, text="Optimize Files & Hardware (Disable Sleep, Block Telemetry, Disable Copilot)", variable=self.opt_var)
        self.opt_cb.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Section 4: Legal & Execution
        self.sec4_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sec4_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.tc_var = ctk.BooleanVar(value=False)
        self.tc_text = (
            "I acknowledge that this program will remove default programs, install software, and requires\n"
            "advanced system access. I agree the creators are not responsible for misuse or data loss."
        )
        self.tc_cb = ctk.CTkCheckBox(self.sec4_frame, text=self.tc_text, variable=self.tc_var, command=self.toggle_forge)
        self.tc_cb.pack(anchor="w", pady=(0, 10))

        self.forge_btn = ctk.CTkButton(
            self.sec4_frame, 
            text="FORGE RETAIL TERMINAL", 
            font=ctk.CTkFont(size=20, weight="bold"), 
            height=50, 
            fg_color="#8B0000", 
            hover_color="#5C0000", 
            state="disabled", 
            command=self.start_forge
        )
        self.forge_btn.pack(fill="x")

        # Section 5: Console
        self.console = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 12))
        self.console.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def toggle_forge(self):
        if self.tc_var.get():
            self.forge_btn.configure(state="normal")
        else:
            self.forge_btn.configure(state="disabled")

    def log(self, msg):
        self.console.configure(state="normal")
        self.console.insert("end", f"{msg}\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def execute_cmd(self, title, cmd):
        self.after(0, self.log, f"\n> {title}")
        self.after(0, self.log, f"$ powershell -Command \"{cmd}\"")
        try:
            process = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                shell=False,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if process.stdout:
                self.after(0, self.log, process.stdout.strip())
            if process.stderr:
                self.after(0, self.log, f"ERROR: {process.stderr.strip()}")
        except Exception as e:
            self.after(0, self.log, f"EXCEPTION: {str(e)}")
        time.sleep(0.5)

    def forge_thread(self, debloat, optimize, pos):
        # Disable UI elements
        self.after(0, self.forge_btn.configure, {"state": "disabled"})
        self.after(0, self.tc_cb.configure, {"state": "disabled"})
        self.after(0, self.log, "=== STARTING PROVISIONING ===")

        # Phase 1: Debloat
        if debloat == "Aggressive":
            cmd = "Get-AppxPackage -AllUsers | Where-Object {$_.Name -notmatch 'Store|Calculator|Photos'} | Remove-AppxPackage"
            self.execute_cmd("Aggressive Debloat", cmd)
        elif debloat == "Basic":
            cmd = "Get-AppxPackage *xbox* | Remove-AppxPackage; Get-AppxPackage *zune* | Remove-AppxPackage"
            self.execute_cmd("Basic Debloat", cmd)

        # Phase 2: Optimization
        if optimize:
            cmd = "powercfg -change -standby-timeout-ac 0; powercfg -change -monitor-timeout-ac 0; Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot' -Name 'TurnOffWindowsCopilot' -Value 1 -Type DWord -Force"
            self.execute_cmd("Applying Optimizations", cmd)

        # Phase 3: POS Install
        if pos != "None" and pos in config.POS_SOFTWARE:
            self.after(0, self.log, f"Executing actual silent install for {pos}...")
            cmd = "; ".join(config.POS_SOFTWARE[pos])
            self.execute_cmd(f"Installing {pos}", cmd)

        # Completion Sequence
        self.after(0, self.log, "\n[!] PROVISIONING COMPLETE.")
        self.after(0, self.setup_reboot_button)

    def setup_reboot_button(self):
        self.forge_btn.configure(
            text="REBOOT SYSTEM", 
            state="normal", 
            fg_color="#006400", 
            hover_color="#004d00", 
            command=self.reboot_system
        )

    def start_forge(self):
        debloat = self.debloat_var.get()
        opt = self.opt_var.get()
        pos = self.pos_var.get()

        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

        # Start execution in background thread
        threading.Thread(target=self.forge_thread, args=(debloat, opt, pos), daemon=True).start()

    def reboot_system(self):
        self.forge_btn.configure(state="disabled")
        self.log("\nInitiating system reboot...")
        subprocess.run("shutdown /r /t 0", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == "__main__":
    app = RetailOSForge()
    app.mainloop()
