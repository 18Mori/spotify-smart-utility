# SpotHash Widget

A minimalist, edge-docked desktop media control widget built with Python and Tkinter. Inspired by Spotify's design aesthetic, SpotHash stays discreetly hidden as a thin green bar on the right side of your screen and expands on hover to grant quick media controls (Previous, Play/Pause, Next, and Exit).

---

## ✨ Features

- **Edge-Docked Floating UI:** Stays pinned on top of other windows (`topmost`).
- **Smooth Hover Transitions:** Expands from a 5px accent bar into a full control strip when hovered over.
- **Global Media Keys:** Sends native OS media commands using the `keyboard` library.
- **Fault-Tolerant Error Handling:** Safely captures media dispatch failures without crashing the UI.
- **Clean Aesthetic:** Dark theme styled around Spotify's signature color palette (`#191414` / `#1DB954`).

---

## 🔮 What's Next? (Coming Soon)

SpotHash is evolving! We are actively upgrading the app to bring richer media integration directly to your desktop.
---

## 📁 Repository Structure

```text
.
├── .gitignore
├── LICENSE
├── requirements.txt
└── app.py              # Main application entry point

```

---

## 🚀 Quick Start & Setup

### 1. Prerequisites

* **Python 3.8+** installed on your system.
* Administrator/Sudo privileges (the `keyboard` library requires low-level access to hook keyboard events).

---

### 2. Clone the Repository

```bash
git clone [https://github.com/your-username/spothash-widget.git](https://github.com/your-username/spothash-widget.git)
cd spothash-widget

```

---

### 3. Set Up a Virtual Environment

#### Windows (PowerShell / CMD)

```cmd
python -m venv venv
source venv\Scripts\activate

```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate

```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🏃 Running the Widget

> **⚠️ Important Notice on Permissions:**
> Because the `keyboard` module monitors global hardware input events, execution may require administrator privileges depending on your OS.

### On Windows

Run PowerShell or Command Prompt **as Administrator**, activate the virtual environment, then launch:

```cmd
python app.py

```

### On Linux

Run with `sudo` pointing to your virtual environment's Python binary:

```bash
sudo ./venv/bin/python app.py

```

---

## 🖥️ Usage

1. Launching the app docks a thin green bar (`#1DB954`) on the top-right corner of your monitor.
2. **Hover** over the bar to reveal the control bar (`⏮`, `⏯`, `⏭`, `✖`).
3. Click any playback button to trigger system-wide media controls.
4. **Move the mouse away** to collapse the widget back into the screen edge.
5. Click **`✖`** to close the application.

---

## 🛠️ Tech Stack

* **GUI Framework:** `tkinter`
* **Global Input Dispatch:** `keyboard`
* **Logging:** Native Python `logging` & `tkinter.messagebox`

---
