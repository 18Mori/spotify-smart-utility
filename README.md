# SpotHash Widget

A minimalist, edge-docked desktop media control widget built with Python and Tkinter. Inspired by Spotify's design aesthetic, SpotHash stays discreetly hidden as a thin green bar on the right side of your screen and expands on hover to grant quick media controls (Previous, Play/Pause, Next), accompanied by a system tray icon in the Windows taskbar for startup management and quitting.

---

## ✨ Features

* **Edge-Docked Floating UI:** Stays pinned on top of other windows (`topmost`) with a clean 3-button control strip (`⏮`, `⏯`, `⏭`).
* **System Tray Integration:** Runs a background system tray icon (next to Wi-Fi and volume) with a context menu to toggle **Launch on System Startup** and **Quit**.
* **Global Media Keys:** Sends native OS media commands using the `keyboard` library.
* **Automatic Audio Ducking:** Automatically lowers Spotify's volume to 15% when other system audio is active, restoring it when audio stops.
* **Persistent User Settings:** Remembers user preferences across launches by storing `settings.json` in a persistent per-user application data directory (`%APPDATA%\SpotHash\` on Windows).
* **Standalone Executable & CI/CD:** Bundled via PyInstaller into a standalone executable with automated GitHub Actions releases.
* **Clean Aesthetic:** Dark theme styled around Spotify's signature color palette (`#191414` / `#1DB954`).

---

## 📁 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yml       # GitHub Actions CI/CD workflow for PyInstaller builds
├── core/
│   ├── __init__.py
│   ├── config.py           # Configuration manager for ignored apps
│   ├── controller.py       # Application lifecycle controller & thread orchestrator
│   ├── duck.py             # Audio session monitoring & auto-ducking logic
│   ├── logger.py           # ANSI-colored console logging formatter
│   ├── settings_manager.py # Persistent user settings manager (AppData/config dir)
│   ├── startup_manager.py  # Cross-platform system startup registration
│   └── tray.py             # System tray icon & taskbar context menu manager
├── UI/
│   ├── __init__.py
│   └── widget.py           # Tkinter edge-docked media widget interface
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── DIRECTORY_LAYOUT.md
├── DEVELOPMENT.md
├── LICENSE
├── main.py                 # Main application entry point
├── requirements.txt
└── ignored_apps.txt        # Default bundled ignored audio processes
```

---

## 🚀 Quick Start & Setup

### 1. Prerequisites

* **Python 3.8+** installed on your system.
* **Windows 10 / 11** (required for `pycaw` audio session control).
* Administrator privileges (the `keyboard` library requires low-level access to hook global media keys).

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/spothash-widget.gif
cd spothash-widget
```

---

### 3. Set Up a Virtual Environment

#### Windows (PowerShell / CMD)
```powershell
python -m venv myenv
.\myenv\Scripts\activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Widget

> **⚠️ Important Notice on Permissions:**
> Because the `keyboard` module monitors global hardware input events, execution may require running your terminal **as Administrator**.

Activate your virtual environment and launch the main orchestrator script:

```cmd
python main.py
```

---

## 🖥️ Usage

1. Launching the app docks a thin green bar (`#1DB954`) on the right edge of your monitor and places an icon in the **Windows system tray** (taskbar notification area next to Wi-Fi/volume).
2. **Hover** over the edge bar to reveal media controls (`⏮`, `⏯`, `⏭`).
3. **Right-click the System Tray Icon** to open the menu:
   * **Launch on System Startup:** Toggle automatic boot startup on/off.
   * **Quit:** Cleanly stop background monitoring, restore Spotify volume, and exit.

---

## 📦 Packaging & Standalone Executable

To bundle SpotHash into a single standalone `.exe` using PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "ignored_apps.txt;." --name="SpotHashWidget" main.py
```
The compiled standalone executable will be located in the `dist/` directory.

---

## 🛠️ Tech Stack

* **GUI Framework:** `tkinter`
* **System Tray:** `pystray` & `Pillow`
* **Audio Session Hooking:** `pycaw` & `pythoncom`
* **Global Input Dispatch:** `keyboard`
* **Startup Management:** `winreg`, `plistlib`, XDG Autostart
* **Concurrency & Persistence:** Native Python `threading`, `logging`, and `json`
