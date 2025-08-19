# FTP Honeypot Setup with vsftpd (Ubuntu + Kali)
# This is a project inside the IEEE Student Branch Team UOI-Arta.

This document describes how we set up an **FTP honeypot** on an Ubuntu machine using **vsftpd**, and tested access from a Kali machine.  
It includes all the steps, trial-and-error issues, and final working configuration.


## Install vsftpd on Ubuntu
```bash
sudo apt update
sudo apt install vsftpd -y
```
### Enable and start service
```bash
sudo systemctl enable vsftpd
sudo systemctl start vsftpd
```


## Initial Configuration
- Edited /etc/vsftpd.conf with the following base settings:
```bash
listen=YES
listen_ipv6=NO
anonymous_enable=YES
local_enable=NO
write_enable=NO
anon_upload_enable=NO
anon_mkdir_write_enable=NO
anon_other_write_enable=NO
anon_root=/srv/ftp
ftpd_banner=Welcome to Ubuntu FTP Server
xferlog_enable=YES
xferlog_file=/var/log/vsftpd.log
log_ftp_protocol=YES
```


## Create Honeypot Directory
- By default, Ubuntu has an ftp user with home /srv/ftp
```bash
sudo mkdir -p /srv/ftp
sudo chown ftp:nogroup /srv/ftp
echo "Welcome to vsftpd honeypot" | sudo tee /srv/ftp/README.txt
```

## First Error - Service Fails
- When restarting:
`sudo systemctl restart vsftpd`-
- Saw:
`status=2/EXITED`
- Fix:
  - The issue was unsupported options in the config.
  - Removed problematic lines like seccomp_sandbox=NO (not supported in my build).
  - After cleanup, vsftpd started successfully.


## Second Error - Chroot Writable
- On connecting from Kali Linux:
`ftp <Ubuntu_IP>`
- Saw:
`500 OOPS: vsftpd: refusing to run with writable root inside chroot()
ftp: Login failed`
- Fix:
  - Option 1: Allow writable chroot in /etc/vsftpd.conf:
      - `allow_writeable_chroot=YES`
  - Option 2: Make /srv/ftp owned by root (non-writable), and create a writable subfolder:
      - ```bash
        sudo chown root:root /srv/ftp
        sudo chmod 755 /srv/ftp
        sudo mkdir -p /srv/ftp/public
        sudo chown ftp:nogroup /srv/ftp/public
        ```
        
## Successful Login from Kali Linux
- Logged in as:
`Name: anonymous | Password: "Enter"`
- Was dropped into /srv/ftp and saw the README.txt file.

## Logs
- vsFTPD logs all activity to: `/var/log/vsftpd.log`
- To watch live: `sudo tail -f /var/log/vsftpd.log`

## Final Notes
- Honeypot allows anonymous login
- Attackers are jailed into /srv/ftp
- No uploads/writes allowed (Read-Only Environment)
- Every login and command attempt is logged
- This makes a simple but effective FTP honeypot for monitoring brute force attempts, enumeration, and attacker behavior
