# Honeypot Script Summary

This Python script implements a simple network honeypot that simulates a fake shell environment for connecting clients. Its main features include:

- **Fake Filesystem:**  
  On startup, the script generates a directory structure (`fake_fs/`) with folders and files mimicking a real Linux system, containing fake sensitive data.

- **TCP Server:**  
  Listens for incoming connections (default port `2222`). Each client is presented with a shell-like prompt.

- **Command Handling:**  
  Supports basic commands such as `ls`, `cat`, `cd`, `pwd`, `uname`, and `whoami`. All other commands return a "Command not found" message.

- **Logging:**  
  Every command entered by a client is logged to `honeypot_log.txt` with a timestamp and client IP address.

- **Session Management:**  
  Each client session starts in the fake `/home/admin` directory and can navigate the fake filesystem.

**Usage:**  
Run the script with Python 3. The honeypot will start listening for connections.  
Clients can connect via `telnet` or `nc` (netcat) to the specified port.

**Disclaimer:**  
This script is for educational and research purposes only. Do not deploy on production systems or expose to the public internet without proper safeguards.
