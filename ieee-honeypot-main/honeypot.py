# Python Script created by Dimitrios Gkarsoudis
import os
import socket
import datetime

LOGFILE = "honeypot_log.txt"
FAKE_FS_DIR = "fake_fs"

# Logging 
def log_action(ip, command):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{timestamp}] {ip} -> {command}\n")

# Fake filesystem
def generate_fake_fs():
    if not os.path.exists(FAKE_FS_DIR):
        os.makedirs(FAKE_FS_DIR)

    structure = {
        "home/admin": ["secrets.txt", "admin.txt"],
        "home/user": ["notes.txt"],
        "etc": ["passwd", "shadow", "hosts"],
        "var/log": ["auth.log", "syslog"],
        "root": ["masterkey.txt"]
    }

    for folder, files in structure.items():
        path = os.path.join(FAKE_FS_DIR, folder)
        os.makedirs(path, exist_ok=True)
        for file in files:
            filepath = os.path.join(path, file)
            if not os.path.exists(filepath):
                with open(filepath, "w") as f:
                    f.write(f"Fake sensitive data inside {file}\n")

# Fake shell
def fake_shell(client_socket, addr):
    ip = addr[0]
    cwd = os.path.join(FAKE_FS_DIR, "home/admin")  # start dir

    client_socket.send(b"Welcome to fake shell!\nType commands, type 'exit' to leave.\n")

    while True:
        prompt = f"{ip}:{cwd.replace(FAKE_FS_DIR, '')}$ "
        client_socket.send(prompt.encode())
        command = client_socket.recv(1024).decode().strip()

        if not command:
            continue

        log_action(ip, command)

        # Commands handling
        if command in ["exit", "quit"]:
            client_socket.send(b"Goodbye!\n")
            break

        elif command.startswith("ls"):
            path = command.replace("ls", "").strip()
            target = os.path.join(cwd, path)
            if os.path.isdir(target):
                files = os.listdir(target)
                client_socket.send(("  ".join(files) + "\n").encode())
            else:
                client_socket.send(b"No such directory\n")

        elif command.startswith("cat"):
            path = command.replace("cat", "").strip()
            target = os.path.join(cwd, path)
            if os.path.isfile(target):
                with open(target, "r") as f:
                    client_socket.send(f.read().encode() + b"\n")
            else:
                client_socket.send(b"No such file\n")

        elif command.startswith("pwd"):
            rel = cwd.replace(FAKE_FS_DIR, "")
            client_socket.send((rel if rel else "/" + "\n").encode())

        elif command.startswith("cd"):
            path = command.replace("cd", "").strip()
            if not path or path == "~":
                cwd = os.path.join(FAKE_FS_DIR, "home/admin")
            else:
                target = os.path.join(cwd, path)
                if os.path.isdir(target):
                    cwd = os.path.normpath(target)
                else:
                    client_socket.send(b"No such directory\n")

        elif command.startswith("uname"):
            client_socket.send(b"Linux honeypot 5.15.0-88-generic #98-Ubuntu SMP x86_64 GNU/Linux\n")

        elif command == "whoami":
            client_socket.send(b"root\n")

        else:
            client_socket.send(b"Command not found in this environment.\n")

    client_socket.close()

# Server snippet
def start_server(host="0.0.0.0", port=2222):
    generate_fake_fs()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Honeypot running on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        fake_shell(client_socket, addr)

if __name__ == "__main__":
    start_server()
