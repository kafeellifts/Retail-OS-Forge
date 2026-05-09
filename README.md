# 🛠️ Retail OS Forge

*Automating the deployment of optimized, bloat-free Point of Sale (POS) terminals.*

---

## 🛑 The Problem Statement

In the retail and small business sector, establishing a dedicated Point of Sale (POS) terminal is a surprisingly manual and frustrating process. When store owners purchase an off-the-shelf Windows machine to run their billing software, they face several hurdles:
1. **Bloatware:** Consumer Windows PCs are loaded with resource-heavy bloatware (Candy Crush, Xbox Game Bar, Cortana) that slow down the machine and distract cashiers.
2. **Interruptive System Behaviors:** Default Windows settings are geared towards personal use. Sleep timers activate during checkout, automated updates force reboots mid-transaction, and telemetry processes consume bandwidth.
3. **Complex Setup:** Installing local, offline-first billing software (which is highly prevalent in India and developing markets) requires manual configuration that non-technical business owners struggle with.

## 💡 The Solution: Retail OS Forge

**Retail OS Forge** is a hardware provisioning utility that solves this problem with a single click. It transforms a standard, bloated Windows installation into a clean, stripped-down, and optimized environment specifically tuned to act as a dedicated retail terminal. 

Instead of spending hours manually configuring settings and uninstalling apps, IT admins or store owners simply select their desired debloat level and POS software, click "Forge," and the application handles the rest using automated PowerShell scripts.

---

## 💻 Tech Stack & Architecture

This application is fundamentally a full-stack Python wrapper around Windows system commands. To demonstrate versatility, the core engine has been implemented across three different UI paradigms:

### 1. The Core Provisioning Engine
- **Python `subprocess`**: The beating heart of the application. It dynamically executes Windows PowerShell commands to modify the Registry, manage `AppxPackages`, and configure PowerCFG settings silently.
- **Threading**: The execution engine runs in background daemon threads to prevent UI freezing while executing long-running system commands.

### 2. The Modern Web-Desktop UI (`forge_app.py`)
- **PyWebview**: Used to spawn a native desktop window that renders a web-based frontend.
- **HTML5 / CSS3 / Vanilla JS**: A beautifully crafted frontend featuring:
  - Complex CSS grid and flexbox layouts.
  - Glassmorphism UI elements with 3D tilt effects.
  - An interactive HTML Canvas particle background.
  - A real-time, simulated terminal that receives live log streams from the Python backend.

### 3. The Traditional Desktop UI (`main.py`)
- **CustomTkinter**: A modern, customizable extension of Python's standard `tkinter` library used to build a lightweight, fast, dark-mode-first native Windows application.

### 4. The REST API Backend (`api_server.py`)
- **FastAPI**: A high-performance Python web framework used to expose the provisioning engine as a web endpoint (`/api/forge`).
- **Uvicorn**: ASGI web server implementation.
- **Server-Sent Events (Streaming)**: The API uses streaming responses to send terminal output line-by-line to external web clients in real-time.

---

## ✨ Key Features

*   **Zero-Touch Debloating**: Automatically executes PowerShell pipelines (`Remove-AppxPackage`) to uninstall default Windows bloatware. Choose between "Basic" (Xbox, Zune) or "Aggressive" (Store, Calculator, Photos, etc.).
*   **Hardware Optimizations**: Edits the Windows Registry (`HKLM`) and Power configurations (`powercfg`) to disable sleep mode, block telemetry, and disable Windows Copilot.
*   **POS Payload Delivery**: Simulates the silent installation and configuration of popular Indian billing software packages (Marg ERP 9+, TallyPrime, Vyapar, Zoho Inventory, Hitech BillSoft).
*   **Live Console Output**: Regardless of the UI chosen, the application intercepts `stdout` from the PowerShell background processes and streams it to the user interface in real-time.

---

## 🚀 Setup & Execution

**⚠️ WARNING: This tool executes commands that uninstall system applications and modify the Windows Registry. Run only on designated target machines, not your personal computer.**

### Prerequisites
- Windows 10/11
- Python 3.8+

### Installation
1. Clone the repository to the target Windows machine.
2. Install the required dependencies:
   ```bash
   pip install customtkinter pywebview fastapi uvicorn
   ```

### Running the Application
You can launch whichever version of the application suits your needs:

*   **Launch the Modern Web UI (Recommended):**
    ```bash
    python forge_app.py
    ```
*   **Launch the Native Desktop UI:**
    ```bash
    python main.py
    ```
*   **Launch the API Server (for headless/remote operation):**
    ```bash
    python api_server.py
    ```

---

## ☁️ Hackathon Deployment Note

Because Retail OS Forge executes **local hardware commands**, standard cloud deployment (like pushing the backend to a free Linux server on Render or Heroku) will fail. Linux servers cannot execute Windows PowerShell commands or edit the Windows Registry.

**To present this at a hackathon, you have two options:**
1. **Simulation Mode:** Modify the `api_server.py` to yield mock terminal strings instead of running `subprocess`. Deploy the API and a web frontend to Vercel/Render to safely demonstrate the architecture to judges.
2. **AWS Windows Server:** Deploy the `api_server.py` onto an AWS EC2 Windows instance. When judges click "Forge" on the web UI, the AWS cloud server will physically execute the debloat commands on itself.

*(For real-world distribution, package `forge_app.py` into a standalone `.exe` using PyInstaller).*
