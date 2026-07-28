Dell Inspiron 5558 Home Server Edition

Target Device

Component	Specification
Device	Dell Inspiron 5558
CPU	Intel Core i7-5500U (2C/4T)
RAM	8GB DDR3L
Internal Storage	240GB SSD
External Storage	1TB Portable HDD
GPU	Intel HD Graphics 5500 + NVIDIA 920M
BIOS	A18
OS	Ubuntu 24.04.1 LTS
Kernel	Linux 6.8
1. Deployment Philosophy

The machine should be treated as:

A low-power always-available home infrastructure server, not a high-performance workstation.

Optimization priorities:

Reliability
Low power consumption
Data safety
Service availability
Performance
2. Final Hardware Architecture
                 Home Network

                      |
                      |
              Router / WiFi

                      |
                      |
          Dell Inspiron 5558 Server

        ┌────────────────────────┐
        │ Ubuntu 24.04 LTS       │
        │                        │
        │ HomeLab OS             │
        └────────────────────────┘

              /            \

       Internal SSD       External HDD

       240GB              1TB
          |                 |
          |                 |
       System            Data
       Docker            Projects
       Database          Backups
       Apps              Media
                         Vault
3. Storage Deployment Plan
Internal SSD (240GB)

Purpose:

Performance workloads

Partition plan:

SSD

/
├── Ubuntu System
│      40GB
│
├── Docker Data
│      80GB
│
├── Database Storage
│      30GB
│
├── HomeLab OS
│      20GB
│
└── Cache / Temporary
       Remaining
External HDD (1TB)

Purpose:

Data storage

Recommended partition:

External HDD

/dev/sdb

├── homelab-storage
│
│   850GB
│
│   ext4
│
│
└── vault
    100GB

    encrypted

Remaining space:

Reserved for filesystem overhead and future expansion.

4. File Structure

External HDD:

/mnt/homelab-storage

├── Projects
│
├── Research
│
├── College
│
├── Documents
│
├── Media
│
├── Downloads
│
├── Backups
│
├── Snapshots
│
└── Vault
5. Linux Optimization
Disable unnecessary services

Check:

systemctl list-unit-files --state=enabled

Disable unused:

Example:

sudo systemctl disable bluetooth

if Bluetooth is not required.

6. CPU Optimization

Your i7-5500U is efficient but limited.

Install:

sudo apt install linux-tools-common linux-tools-generic

Monitor:

cpupower frequency-info
CPU Governor

For normal mode:

powersave

For development:

performance

Profiles:

HomeLab OS

Power Saving
      |
      |
Balanced
      |
      |
Performance
7. RAM Optimization

8GB RAM is workable but needs control.

Install:

ZRAM

Very recommended.

sudo apt install zram-tools

Why:

Instead of immediately using slow swap:

RAM
 |
compressed memory
 |
SSD swap

This improves responsiveness.

Recommended:

RAM:
8GB

ZRAM:
2-3GB

SSD Swap:
4GB
8. Docker Resource Limits

Important.

Do not allow containers to consume everything.

Example:

Gitea

RAM:
512MB


PostgreSQL

RAM:
1GB


Monitoring

RAM:
512MB

Docker policy:

Core Services

Always running


Heavy Services

Only when workspace starts
9. External HDD Optimization
Mount Options

Use:

noatime

Benefits:

Less disk writes.
Longer HDD life.

Example:

UUID=/xxxx

/mnt/storage

ext4

defaults,noatime
10. HDD Health Monitoring

Install:

sudo apt install smartmontools

Enable:

sudo systemctl enable smartd

Monitor:

Temperature
Bad sectors
Read errors
Power cycles

HomeLab OS Alert:

HDD Health

95%
Healthy


Warning:

Reallocated sectors increasing
11. Power Management Design

Your requirement:

Server should conserve power when not working.

We implement three layers.

Layer 1: Service Power

Stop unnecessary services.

Example:

Night:

Docker Development Containers
        |
        OFF

Running:

SSH
Monitoring
Storage
Layer 2: Sleep Schedule

Example profile:

Developer Schedule
09:00

Wake


09:00-00:00

Normal operation


00:00

Sleep
Vacation Mode
Only:

SSH
Backup
Health Monitor
Layer 3: Wake System

Possible technologies:

Wake-on-LAN

Check:

ethtool eth0

If supported:

Laptop sleeping

↓

Wake packet

↓

Server starts
12. BIOS Configuration

Recommended BIOS settings:

Enable
Virtualization Technology

Required for:

Containers
Future VMs
Power Settings

Enable:

Wake on AC

if available.

Disable

Unused:

PXE Boot
Unused devices
13. Network Configuration
Static IP

Do not rely on DHCP.

Example:

Server:

192.168.1.50

Services:

dashboard.home

git.home

docs.home
14. Security Deployment
Firewall

Install:

sudo apt install ufw

Default:

DENY incoming
ALLOW outgoing

Allow:

SSH:

22

HomeLab:

80
443
15. Remote Access

Do NOT expose:

SSH
Samba
Dashboard

directly.

Future:

Remote Device

      |

VPN

      |

HomeLab OS

Recommended:

WireGuard
Tailscale
16. Backup Strategy

Current:

SSD

↓

External HDD

Future:

Add second backup drive.

Ideal:

Server SSD

      ↓

External HDD

      ↓

Offline HDD
17. Deployment Software Stack

Initial installation:

Ubuntu

↓

Updates

↓

Docker

↓

HomeLab OS Core

↓

PostgreSQL

↓

Dashboard

↓

Storage Manager

↓

Vault Manager

↓

Automation
18. First Boot Checklist

After preparing the server:

System

☐ Ubuntu updated
☐ Hostname changed
☐ Static IP configured
☐ SSH enabled
☐ Firewall enabled

Storage

☐ HDD detected
☐ Partition created
☐ Mounted automatically
☐ SMART enabled
☐ Vault created

Development

☐ Docker installed
☐ Docker Compose installed
☐ Git installed
☐ Python environment ready

HomeLab OS

☐ Repository cloned
☐ Database created
☐ Backend running
☐ Dashboard accessible

19. Recommended Future Hardware Upgrades
Priority 1
RAM upgrade

From:

8GB

to:

16GB DDR3L

Impact:

★★★★★

This is the biggest improvement.

Priority 2

Replace SSD:

240GB

with:

500GB/1TB SSD

Impact:

★★★★☆

Priority 3

Second external HDD

Purpose:

Backup redundancy.

Impact:

★★★★★

Priority 4

UPS

Purpose:

Prevent corruption.
Clean shutdown.
Protect HDD.
Final Deployment Architecture
                 HomeLab OS

                      |
              Ubuntu 24.04 LTS

                      |
        ┌─────────────┴─────────────┐

        SSD                         HDD

        OS                          Data
        Docker                      Projects
        Database                    Backup
        Apps                        Vault
                                    Snapshots


                      |

             Docker Platform

                      |

        Core + Development + Storage
        + Automation + Monitoring
Phase 0 Status

Completed:

✅ SRS
✅ Architecture
✅ Database Design
✅ API Specification
✅ UI Wireframe
✅ Security Model
✅ Repository Structure
✅ Development Setup
✅ Docker Architecture
✅ Implementation Roadmap
✅ Hardware Optimization Plan