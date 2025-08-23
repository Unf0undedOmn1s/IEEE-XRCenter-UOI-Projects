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
- This makes a simple but effective FTP honeypot for monitoring brute force attempts, enumeration, and attacker behavior **EDITED: 19/08/2025**


We encountered several issues during the setup, documented below step by step, including trial-and-error actions, errors, and resolutions attempted.


## Initial SSH Installation
1. Installed the OpenSSH server:
```bash
sudo apt update
sudo apt install openssh-server
```
2. Verified the service:
`systemctl status ssh`
- Outcome: Service appeared active, running.
3. Checked listening ports:
`ss -tulnp | grep ssh`
- Outcome: No output initially, causing confusion.
4. Attempted connecting locally from Ubuntu:
`ssh localhost`
- Outcome: Connection Refused.


## Firewall and Networking Checks
1. Checked ufw status
`sudo ufw status`
- Outcome: Inactive, so firewall was not blocking it.
2. Checked SSH listening with netstat/ss:
` ss- tulnp | grep 22`
- Outcome: Initially nothing, then confirmed SSH running after a restart.
3. Tried connecting from Kali Linux machine (Same Network)
`ssh <USER>@<IP>
- Outcome: Connection refused by peer.
- Possible causes investigated:
  - Firewall issues -> UFW inactive
  - Service misconfiguration -> Confirmed running
  - Network restrictions -> Suspected router blocking


## Remote Access Attempts
1. Tried SSH remote forwarding to a public server:
`ssh -R 2222:localhost:22 <USER@<PUBLIC-IP>`
- Outcome: Connection refused
- Problem: Did not have access to a public server or NAT configuration for port forwarding.
2. Attempted using Ngrok TCP Tunnel:
`ngrok tcp 22`
- Outcome: Failed due to free account restrictions.
3. Attempted using Cloudflare Tunnel (`cloudflared`):
`cloudflared tunnel --url ssh://localhost:22`
- Errors encountered:
  - ICMP proxy warnings (ping_group_range issue)
  - Missing origin certificate (cert.pem not found)
  - UDP buffer warnings
- Outcome: Tunnel partially established but could not get usable endpoint for SSH access.


## Final Status
- FTP Honeypot works locally on ubuntu.
- Remote acccess blocked by router restrictions.
- Project to be finalized once machines are on the same network with colleague:
- Dimitrios-Nikolaos-Gkarsoudis <https://github.com/Dimitrios-Nikolaos-Gkarsoudis>


## Fake File System Integration by Dimitios Gkarsoudis
Created a script generating fake files at:
- `/home/honeypotieee/Downloads/fake_fs`


## Linked directory into FTP root:
```bash
sudo ln -s /home/honeypotieee/Downloads/fake_fs /srv/ftp/fake_fs
```
- Set proper permissions:
  - `sudo chown -R ftp:ftp /srv/ftp/fake_fs`
  - `sudo chmod -R 755 /srv/ftp/fake_fs`
- Restarted vsFTPD:
  -`sudo systemctl restart vsftpd`
- Confirmed via FTP on Kali Linux machine:
  - `ftp> cd fake_fs`
    `ftp> ls`


## Conclusion
Although we could not fully set up remote SSH access for external users, this exercise provided important insights into network restrictions, firewall configurations, and tunneling solutions for secure honeypot deployment. All commands, errors, and trial-and-error steps are documented above for reference and reproducibility. **EDITED: 22/08/2025**


## Lessons Learned/Observations
1. Setting up SSH is straightforward locally, but exposing it over the internet requires:
- Public server or tunneling service
- Proper firewall and router/NAT configuration
- Service configuration (sshd_config) for secure access
2. Free services like Ngrok limit TCP usage, making remote access harder.
3. cloudflared requires proper configuration and certificates to function as a tunnel for SSH.
4. Debugging Tips:
- Always check which process listens on port 22:
  - `ss -tulnp | grep 22`
- Verify firewall or router rules
- Use nc or telnet to quickly test connectivity:
  -`nc -vz ubuntu_ip 22`


## Next Steps (Future Improvements)
1. Test final deployment on the same network for full functionality.
2. Optionally integrate:
  - Splunk for log analysis.
