Initial Ubuntu Server Preparation Script

This script performs only safe base preparation.

It does NOT:

Format disks
Create vaults
Modify partitions
Change BIOS

Those require manual verification.

Create:

prepare_homelab.sh

Content:

#!/bin/bash

set -e

echo "================================"
echo " HomeLab OS Preparation Script"
echo "================================"


echo "[1] Updating system"

sudo apt update
sudo apt upgrade -y


echo "[2] Installing packages"

sudo apt install -y \
git \
curl \
wget \
nano \
vim \
htop \
tree \
net-tools \
openssh-server \
smartmontools \
lm-sensors \
ufw \
docker.io \
docker-compose-v2 \
tlp \
zram-tools


echo "[3] Enable Services"

sudo systemctl enable ssh
sudo systemctl enable docker
sudo systemctl enable tlp


echo "[4] Docker User Setup"

sudo usermod -aG docker $USER


echo "[5] Firewall Setup"

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443


echo "[6] Creating directories"


sudo mkdir -p /opt/homelab-os
sudo mkdir -p /srv/homelab


mkdir -p ~/homelab

mkdir -p ~/homelab/docker
mkdir -p ~/homelab/configs
mkdir -p ~/homelab/logs
mkdir -p ~/homelab/backups


echo "[7] Docker Test"

docker --version


echo "[8] System Information"

echo ""
echo "CPU:"
lscpu | grep "Model name"

echo ""

echo "RAM:"
free -h

echo ""

echo "Storage:"
df -h


echo ""
echo "================================"
echo " Preparation Complete"
echo " Reboot recommended"
echo "================================"

Run:

chmod +x prepare_homelab.sh

Execute:

./prepare_homelab.sh

Then:

sudo reboot
Deployment Status

After completing this:

Your Dell Inspiron 5558 becomes:

Ubuntu Base Server
        |
        |
 Docker Ready
        |
        |
 Storage Ready
        |
        |
 HomeLab OS Ready