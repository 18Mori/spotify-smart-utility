# SpotHash Widget

A minimalist, edge-docked desktop media control widget built with Python and Tkinter. Inspired by Spotify's design aesthetic, SpotHash stays discreetly hidden as a thin green bar on the right side of your screen and expands on hover to grant quick media controls (Previous, Play/Pause, Next, System Startup Toggle, and Exit) alongside automatic Spotify audio ducking.

---

## ✨ Features

* **Edge-Docked Floating UI:** Stays pinned on top of other windows (`topmost`).
* **Smooth Hover Transitions:** Expands from a 5px accent bar into a full control strip when hovered over.
* **Global Media Keys:** Sends native OS media commands using the `keyboard` library.
* **Automatic Audio Ducking:** Automatically lowers Spotify's volume to 15% when other system audio is active, restoring it when audio stops.
* **System Startup Integration:** Dedicated `🚀` startup toggle button allowing users to register/unregister the app to launch on system boot (Windows Registry, macOS LaunchAgents, Linux XDG autostart).
* **Settings Persistence:** Remembers user preferences locally via JSON (`settings.json`).
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
│   ├── settings_manager.py # Local JSON settings persistence
│   └── startup_manager.py  # Cross-platform system startup registration
├── UI/
│   ├── __init__.py
│   └── widget.py           # Tkinter edge-docked widget interface & controls
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── DIRECTORY_LAYOUT.md
├── DEVELOPMENT.md
├── LICENSE
├── main.py                 # Main application entry point
├── requirements.txt
├── ignored_apps.txt
└── settings.json           # Local user preference storage
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
git clone https://github.com/your-username/spothash-widget.git
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

1. Launching the app docks a thin green bar (`#1DB954`) on the right edge of your monitor.
2. **Hover** over the bar to reveal the control bar (`⏮`, `⏯`, `⏭`, `🚀`, `✖`).
3. Click any playback button (`⏮`, `⏯`, `⏭`) to trigger system-wide media controls.
4. Click the **`🚀`** button to toggle **Launch on System Startup** (green = enabled, gray = disabled).
5. **Move the mouse away** to collapse the widget back into the screen edge.
6. Background audio monitoring automatically ducks Spotify when external audio plays.
7. Click **`✖`** to cleanly terminate background threads, restore original Spotify volume, and exit.

---

## 📦 Packaging & Standalone Executable

To bundle SpotHash into a single standalone `.exe` using PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile --name="SpotHashWidget" main.py
```
The compiled standalone executable will be located in the `dist/` directory.

---

## 🛠️ Tech Stack

* **GUI Framework:** `tkinter`
* **Audio Session Hooking:** `pycaw` & `pythoncom`
* **Global Input Dispatch:** `keyboard`
* **Startup Management:** `winreg`, `plistlib`, XDG Autostart
* **Concurrency & Persistence:** Native Python `threading`, `logging`, and `json`
