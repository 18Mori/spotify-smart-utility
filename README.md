# SpotHash Widget

A minimalist, edge-docked desktop media control widget built with Python and Tkinter. Inspired by Spotify's design aesthetic, SpotHash stays discreetly hidden as a thin green bar on the right side of your screen and expands on hover to grant quick media controls (Previous, Play/Pause, Next, and Exit) alongside automatic Spotify audio ducking.

---

## ✨ Features

* **Edge-Docked Floating UI:** Stays pinned on top of other windows (`topmost`).
* **Smooth Hover Transitions:** Expands from a 5px accent bar into a full control strip when hovered over.
* **Global Media Keys:** Sends native OS media commands using the `keyboard` library.
* **Automatic Audio Ducking:** Automatically lowers Spotify's volume to 15% when other system audio is active, restoring it when audio stops.
* **Fault-Tolerant Error Handling:** Safely captures media dispatch and audio session failures without crashing the UI.
* **Clean Aesthetic:** Dark theme styled around Spotify's signature color palette (`#191414` / `#1DB954`).

---

## 🔮 What's Next? (Coming Soon)

SpotHash is still evolving! We are actively upgrading the app to bring richer media integration directly to your desktop.

---

## 📁 Repository Structure

```text
.
├── core/
│   ├── __init__.py
│   └── duck.py         # Audio session monitoring & auto-ducking logic
├── ui/
│   ├── __init__.py
│   └── widget.py       # Tkinter edge-docked widget interface
├── .gitignore
├── README.md
├── LICENSE
├── main.py             # Main application entry point & thread orchestrator
└── requirements.txt

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
python -m venv venv
.\venv\Scripts\activate

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

1. Launching the app docks a thin green bar (`#1DB954`) on the top-right edge of your monitor.
2. **Hover** over the bar to reveal the control bar (`⏮`, `⏯`, `⏭`, `✖`).
3. Click any playback button to trigger system-wide media controls.
4. **Move the mouse away** to collapse the widget back into the screen edge.
5. Background audio monitoring automatically ducks Spotify when external audio plays.
6. Click **`✖`** to cleanly terminate background threads, restore original Spotify volume, and exit.

---

## 🛠️ Tech Stack

* **GUI Framework:** `tkinter`
* **Audio Session Hooking:** `pycaw` & `pythoncom`
* **Global Input Dispatch:** `keyboard`
* **Concurrency:** Native Python `threading` & `logging`

---
