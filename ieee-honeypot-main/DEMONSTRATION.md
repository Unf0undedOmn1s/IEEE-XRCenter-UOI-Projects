# Honeypot Services Demonstration

## 1. FTP Service (vsftpd)
### What it Does
- Provides file transfer access between client and server.
- Used in honeypots to lure attackers into interacting with fake data.

### Requirements
- `vsftpd` installed and running.
- Proper directory structure with correct permissions.
- Firewall allows FTP ports (21 for control, passive range for data).

### Key Commands
```bash
# Install vsftpd
sudo apt update && sudo apt install vsftpd -y
```

# Start and enable service
`sudo systemctl start vsftpd`
`sudo systemctl enable vsftpd`

# Check status
`sudo systemctl status vsftpd`

# FTP Client Usage
```bash
ftp <server_ip>
ls        # List files
cd <dir>  # Change directory
get <file> # Download file
put <file> # Upload file (if allowed)
```


## 2. Secure Shell (SSH)
### What it Does
- Allows secure remote access to a server via encrypted connection.
- Used for administration and (in honeypots) can be monitored for brute-force attempts.
- **Requirements**
    - openssh-server installed and running on target system.
    - Proper firewall rules (TCP port 22 open by default).
### Key Commands
# Install SSH Server
`sudo apt update && sudo apt install openssh-server -y`
# Start and enable SSH
`sudo systemctl start ssh`
`sudo systemctl enable ssh`
# Check if SSH is running
`sudo systemctl status ssh`
# Connect to server
`ssh user@server_ip`
# Example: Tunneling FTP over SSH
`ssh -L 2121:localhost:21 user@server_ip`


## 3. Fake File System
### What it Does
- Creates a realistic directory structure with dummy data to mislead attackers.
- Used to study attacker behavior while protecting real assets.
- **Requirements**
  - A directory containing generated fake files.
  - Symlink or direct placement into FTP root.
  - Correct permissions for FTP to access.

## Setup Example
```bash
# Fake filesystem path
/home/honeypotieee/Downloads/fake_fs

# Link fake FS to FTP root
sudo ln -s /home/honeypotieee/Downloads/fake_fs /srv/ftp/fake_fs

# Adjust permissions
sudo chown -R ftp:ftp /srv/ftp/fake_fs
sudo chmod -R 755 /srv/ftp/fake_fs

# Restart FTP to apply changes
sudo systemctl restart vsftpd
```

## Verification
```bash
ftp <server_ip>
cd fake_fs
ls
```

## 4. What it takes Services to work
- vsftpd: Needs correct configuration, open ports, and readable/writable directories.
- SSH: Needs active service, firewall access, and proper authentication.
- Fake FS: Must be accessible to FTP user with proper permissions.

