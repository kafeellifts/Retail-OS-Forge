#  Retail OS Forge

Hey there! Welcome to **Retail OS Forge**. 

If you've ever had to set up a Windows machine to act as a dedicated Point of Sale (POS) terminal, you know it's a huge pain. You have to uninstall all the random Windows bloatware (looking at you, Candy Crush and Xbox Game Bar), dive into settings to stop the computer from going to sleep right when a customer is paying, and then finally install the actual billing software. 

I built this tool to automate all of that. You just click a few buttons, and it turns a standard, bloated Windows installation into a clean, optimized, and ready-to-go retail terminal.

##  What this actually does

Under the hood, this is a Python app that runs Windows PowerShell commands to get the job done. It handles three main things:

1. **Debloating**: Rips out unnecessary Windows apps. You can choose a "Basic" clean or go "Aggressive".
2. **Hardware Optimizations**: Disables sleep mode, turns off telemetry, and disables Windows Copilot so the machine focuses purely on running your store.
3. **POS Setup**: Simulates the silent installation of popular Indian billing software (like Marg ERP, TallyPrime, Vyapar, etc.).

##  How it's built

I experimented with a few different ways to build this, so you'll actually find a couple of different "versions" of the app in this repo:

* **The Web-UI Version (`forge_app.py`)**: This is the coolest one. It uses `pywebview` to launch a native desktop window, but the UI is built with HTML/CSS/JS. It has a super sleek dark mode, cool glassmorphism effects, and a live terminal that streams the output.
* **The Traditional Desktop App (`main.py` & `retail_os_forge.py`)**: Built entirely in Python using `customtkinter`. It's lightweight and gets straight to the point.
* **The API Backend (`api_server.py`)**: A FastAPI server that exposes the provisioning engine as a REST endpoint. Useful if you want to trigger setups remotely!

##  How to run it locally

Since this app literally alters Windows system files and uninstalls programs, **run it at your own risk!** It's designed for fresh machines you want to convert into terminals, not your personal gaming rig.

1. Make sure you have Python installed.
2. Install the required libraries (you'll need things like `customtkinter`, `pywebview`, and `fastapi` depending on which version you run).
3. To launch the shiny web-UI version, run:
   ```bash
   python forge_app.py
   ```
4. To launch the standard Python UI, run:
   ```bash
   python main.py
   ```
   *(or `python retail_os_forge.py` for the standalone version)*

##  A quick note on "Deploying" this

If you're looking at this for a hackathon and want to deploy it to the cloud—be careful! The backend executes local Windows PowerShell commands. If you put the backend on a free Linux server (like Render), it won't work because Linux doesn't understand PowerShell or Windows Registries. 

This is fundamentally a **local hardware tool**. The best way to "distribute" it is to package it into an `.exe` file using PyInstaller and put it on a flash drive!

---

Feel free to poke around the code, fork it, or use the engine to build your own custom setup scripts. Happy forging! 
