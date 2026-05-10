# Retail OS Forge

## The Problem in the Retail Tech Sector
A non-tech retailer often doesn't know how to optimize a standard consumer PC for a dedicated business environment. They purchase off-the-shelf Windows machines that are loaded with consumer bloatware, distractive features, and unoptimized power settings, making the setup of a reliable Point of Sale (POS) terminal a daunting and error-prone task.

## How Our Program Solves It
Retail OS Forge solves this by compiling all the individual, complex IT operations one would normally have to do manually into one single, one-click program. It automatically debloats the OS, configures registry settings, and installs necessary software, optimizing the device purely for business purposes.

## Business Benefits
- **Zero IT Dependency:** Store owners don't need to hire expensive IT technicians to set up their computers.
- **Maximized Performance:** By stripping away consumer apps and background processes, all system resources (CPU, RAM) are dedicated to the POS software, ensuring fast checkouts.
- **Standardization:** Eliminates human error and ensures every terminal across multiple store locations is configured identically.
- **Reduced Downtime:** Optimized settings prevent memory leaks and system crashes during peak retail hours.

## Future Potential
Currently, Retail OS Forge is a single-role prototype focused on POS terminals. However, we can integrate this onto different roles such as:
- Banking computers
- Cashier computers
- Hospital receptionist computers

This provides immense relief for the business owner, as they do not have to depend on anyone for installing and optimizing their computer for its specific role.

---

## Debloat Operations

### Basic Debloat
The Basic option safely removes the most common, unused consumer bloatware:
- Microsoft Bing
- Microsoft Zune

### Aggressive Debloat
The Aggressive option performs a deep system sweep, removing almost all Universal Windows Platform (UWP) apps to create a sterile, hyper-focused environment.
- **Removed:** All non-essential built-in Windows applications.
- **Retained:** Microsoft Store is kept intact to allow for necessary framework updates.

---

## Supported POS Software
The program features **live, fully automated silent installations**. When a POS is selected, the engine uses PowerShell (`Invoke-WebRequest` and `Start-Process`) to automatically download the official installer to a temporary directory and execute it silently in the background, requiring zero user interaction. We currently support:
- **Marg ERP 9+**
- **TallyPrime**
- **Busy Accounting**
- **Vyapar**
- **Zoho Inventory** *(Automatically provisions a dedicated web-app desktop shortcut)*
- **Hitech BillSoft**

---

## System Optimizations
The program applies the following system-level optimizations:
- **ClearPageFileAtShutdown:** Modifies the Windows Registry (`HKLM:\System\CurrentControlSet\Control\Session Manager\Memory Management`) to clear the system page file upon every shutdown. This ensures that sensitive data is flushed from virtual memory and helps prevent memory corruption over long system uptimes.

---

## Tech Stack
- **Python 3:** The core logic, background threading, and OS interaction layer.
- **PowerShell:** The underlying execution engine responsible for uninstallation sweeps and deep registry modifications.
- **CustomTkinter:** Used for the robust, dark-themed native Windows GUI application (`main.py`).
- **pywebview:** Provides a native Windows wrapper to render the web-based frontend (`forge_app.py`).
- **HTML5, CSS3, Vanilla JavaScript:** Drives the modern web interface, including 3D tilt effects and dynamic HTML Canvas backgrounds.
- **FastAPI & Uvicorn:** Powers the REST API engine (`api_server.py`) allowing for headless execution and network-based terminal provisioning.

---

## Getting Started

### Prerequisites
- **Operating System:** Windows 10 or 11
- **Python:** Python 3.7 or higher installed

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/kafeellifts/Retail-OS-Forge.git
   cd Retail-OS-Forge
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment, but you can install them globally:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To start the Retail OS Forge utility, run the following command in your terminal:
```bash
python main.py
```

> [!IMPORTANT]
> **Admin Privileges:** The application needs to modify registry settings and remove system packages. It will automatically attempt to restart with Administrator privileges if needed.

### Project Structure
- `main.py`: The primary entry point (Basic UI).
- `forge_app.py`: The Modern "Neon" UI version.
- `api_server.py`: The headless API server version.
- `config.py`: Centralized configuration for all commands and software links.
