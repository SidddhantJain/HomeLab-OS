Dell Inspiron 5558 Production Installation Checklist

This document describes the actual physical and software deployment process before HomeLab OS Phase 1 development begins.

The goal:

Transform your Dell Inspiron 5558 into a reliable:

Development server
Personal cloud
Backup server
Storage server
Automation server
Part 1 — Pre-Deployment Checklist
Hardware Checklist
Server Laptop

☑ Dell Inspiron 5558
☑ i7-5500U
☑ 8GB RAM
☑ 240GB SSD
☑ NVIDIA 920M
☑ Intel HD Graphics 5500

External Hardware

☑ 1TB Portable HDD

Recommended:

USB 3.0 port
Dedicated cable
Stable power connection
Optional Future Hardware

Priority:

1. RAM Upgrade

Current:

8GB

Recommended:

16GB DDR3L

Impact:

★★★★★

2. UPS

Protect:

HDD
SSD
Database

Impact:

★★★★★

Part 2 — BIOS Preparation

Enter BIOS:

F2 during boot
BIOS Settings
Enable
Virtualization
Intel Virtualization Technology
        ENABLED

Required for:

Docker
Virtual machines
Wake Features

Enable if available:

Wake on AC
Wake on LAN
Disable

Unused:

PXE Boot
Unused Boot Devices
Part 3 — Ubuntu Base Preparation

Current OS:

Ubuntu 24.04.1 LTS

Keep it.

No need to reinstall immediately.

Update system:

sudo apt update
sudo apt upgrade -y

Install essential tools:

sudo apt install -y \
curl \
wget \
git \
nano \
vim \
htop \
tree \
net-tools \
openssh-server \
smartmontools \
lm-sensors \
ufw
Part 4 — Server Identity Setup

Change hostname:

Example:

homelab-server

Command:

sudo hostnamectl set-hostname homelab-server

Check:

hostname

Expected:

homelab-server
Part 5 — Create Server User Model

Do not run everything as root.

Create:

homelab-admin

Command:

sudo adduser homelab-admin

Give admin rights:

sudo usermod -aG sudo homelab-admin

Create service directories:

sudo mkdir -p /opt/homelab
sudo mkdir -p /srv/homelab

Structure:

/
|
├── opt
│   └── homelab
│
└── srv
    └── homelab
Part 6 — Network Configuration
Find current IP
ip addr

Example:

192.168.1.50
Recommended

Reserve this IP in router:

homelab-server

192.168.1.50

Reason:

Services depend on fixed addressing.

Part 7 — SSH Configuration

Install:

sudo apt install openssh-server

Enable:

sudo systemctl enable ssh
sudo systemctl start ssh

Test:

From another device:

ssh username@192.168.1.50
Security

Edit:

sudo nano /etc/ssh/sshd_config

Change:

PermitRootLogin no

Restart:

sudo systemctl restart ssh
Part 8 — Firewall Setup

Enable firewall:

sudo ufw enable

Default:

sudo ufw default deny incoming
sudo ufw default allow outgoing

Allow SSH:

sudo ufw allow ssh

Allow future web services:

sudo ufw allow 80
sudo ufw allow 443

Check:

sudo ufw status
Part 9 — External HDD Setup
Identify Disk

Connect HDD.

Run:

lsblk

Example:

sda
 └─ Ubuntu SSD

sdb
 └─ 1TB HDD
IMPORTANT

Verify the disk.

Do NOT format the wrong drive.

Partition Layout

Target:

1TB HDD

/dev/sdb1

850GB

ext4

Normal Storage


/dev/sdb2

100GB

Encrypted Vault
Create Storage Partition

Example:

sudo fdisk /dev/sdb

Create:

/dev/sdb1

Format:

sudo mkfs.ext4 /dev/sdb1
Create Mount Point
sudo mkdir /mnt/homelab-storage

Mount:

sudo mount /dev/sdb1 /mnt/homelab-storage
Permanent Mount

Find UUID:

blkid

Edit:

sudo nano /etc/fstab

Add:

UUID=<disk-id> 
/mnt/homelab-storage
ext4
defaults,noatime
0 2

Test:

sudo mount -a
Part 10 — Vault Creation

Your requirement:

100GB encrypted vault

Recommended technology:

LUKS encryption

Install:

sudo apt install cryptsetup

Create partition:

/dev/sdb2

Encrypt:

sudo cryptsetup luksFormat /dev/sdb2

Open:

sudo cryptsetup open /dev/sdb2 homelab-vault

Create filesystem:

sudo mkfs.ext4 /dev/mapper/homelab-vault

Mount:

sudo mkdir /mnt/vault
sudo mount /dev/mapper/homelab-vault /mnt/vault

Lock:

sudo umount /mnt/vault
sudo cryptsetup close homelab-vault

Result:

Vault

🔒 Locked

Password required
Part 11 — Install Docker

Install:

sudo apt install docker.io docker-compose-v2

Enable:

sudo systemctl enable docker

Add user:

sudo usermod -aG docker $USER

Logout/login.

Test:

docker run hello-world
Part 12 — Docker Directory Setup

Create:

mkdir -p ~/homelab/docker

Structure:

~/homelab

├── docker
│
├── configs
│
├── backups
│
└── logs
Part 13 — Install Monitoring Tools

Hardware monitoring:

sudo apt install \
lm-sensors \
smartmontools

Detect sensors:

sudo sensors-detect

Test:

sensors
Part 14 — Power Optimization

Install:

sudo apt install tlp

Enable:

sudo systemctl enable tlp

Check:

sudo tlp-stat
Part 15 — ZRAM Setup

Install:

sudo apt install zram-tools

Check:

swapon --show

Expected:

/dev/zram0
Part 16 — Automatic Updates

Install:

sudo apt install unattended-upgrades

Enable:

sudo dpkg-reconfigure unattended-upgrades
Part 17 — Initial Folder Structure

After deployment:

/mnt/homelab-storage

├── Projects
│
├── Backups
│
├── Snapshots
│
├── Downloads
│
├── Documentation
│
├── Media
│
└── Shared


/mnt/vault

├── Private Documents
├── Passwords
├── Certificates
└── Sensitive Data
Part 18 — Initial Health Test

Run:

CPU
htop
RAM
free -h
Storage
df -h
Disk Health
sudo smartctl -a /dev/sdb
Network
ping google.com
Part 19 — HomeLab OS Installation Location

Final:

Ubuntu
 |
 |
 /opt/homelab-os

HomeLab OS Application


Docker

 |
 |
 /srv/homelab

Persistent Data


External HDD

 |
 |
 /mnt/homelab-storage

User Data
Part 20 — Deployment Completion Checklist
Base System

☐ Ubuntu updated
☐ Hostname configured
☐ Admin user created
☐ SSH working
☐ Firewall enabled

Storage

☐ HDD detected
☐ Storage partition created
☐ Auto mount enabled
☐ Vault encrypted
☐ Vault tested

Performance

☐ ZRAM enabled
☐ TLP enabled
☐ Docker installed
☐ SMART monitoring enabled

Ready for HomeLab OS

☐ Repository created
☐ Database ready
☐ Docker environment ready

