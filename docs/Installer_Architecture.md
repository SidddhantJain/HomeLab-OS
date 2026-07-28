# HomeLab OS Installer Architecture

This document details the dual-installer architecture used for deploying HomeLab OS.

---

## 💡 Dual-Installer Strategy

Because HomeLab OS is designed to run on a Linux server (Dell Inspiron 5558 / Ubuntu 24.04 LTS), but developers and home lab administrators often manage servers from a Windows laptop, HomeLab OS provides two specialized installer paths:

```text
                  ┌───────────────────────────────┐
                  │    HomeLab OS Installers      │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│   Windows Remote Assistant      │       │     Linux Native Installer      │
│     (installer/windows/)        │       │       (installer/linux/)        │
└────────────────┬────────────────┘       └────────────────┬────────────────┘
                 │                                         │
                 │ Connects over SSH                       │ Runs directly on
                 ▼                                         ▼ target server
┌──────────────────────────────────────────────────────────────────────────┐
│                   Target Ubuntu Server Runtime                           │
│                   (/deployment/install.sh)                               │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ 1. Windows Remote Installation Assistant (`installer/windows/`)

- **Role**: Remote wizard and server provisioner.
- **Key Actions**:
  - Discovers Ubuntu servers on the local subnet via mDNS (`homelab.local`) or IP scan.
  - Establishes an SSH connection to the server.
  - Interactively prompts user for admin credentials and drive mounts.
  - Uploads code bundle and executes `/deployment/install.sh` on the server over SSH.

---

## 🐧 2. Native Linux Server Installer (`installer/linux/`)

- **Role**: Direct server installer.
- **Key Actions**:
  - Executed directly on the Ubuntu server console or via SSH terminal.
  - Runs `/deployment/requirements_check.sh` to check RAM, Disk, Docker.
  - Provisions `/opt/homelab`, `/var/log/homelab`, `/mnt/storage`, `/mnt/vault`.
  - Runs `docker compose up -d --build`.
  - Runs `/deployment/health_check.sh`.
