# HomeLab OS Deployment Pipeline Architecture

This document describes the end-to-end lifecycle pipeline for HomeLab OS, from code commit to server execution.

---

## 🏗️ Pipeline Flow Architecture

```text
┌─────────────────────────┐
│   Developer Machine     │  (Environment 1: Code, Test, Build)
└────────────┬────────────┘
             │
             ▼  git push origin main
┌─────────────────────────┐
│     Git Repository      │  (GitHub Source Control)
└────────────┬────────────┘
             │
             ▼  release/package.sh
┌─────────────────────────┐
│     Release Package     │  (Versioned Tarball Bundle: release/packages/homelab-os-v1.0.0.tar.gz)
└────────────┬────────────┘
             │
             ▼  installer/windows or installer/linux
┌─────────────────────────┐
│        Installer        │  (Remote Assistant / Native Linux Script)
└────────────┬────────────┘
             │
             ▼  ssh / local execution
┌─────────────────────────┐
│     HomeLab Server      │  (Environment 2: Dell Inspiron 5558 / Ubuntu 24.04 LTS)
└────────────┬────────────┘
             │
             ▼  deployment/install.sh
┌─────────────────────────┐
│     Docker Runtime      │  (Docker Engine & Docker Compose)
└────────────┬────────────┘
             │
             ▼  docker compose up -d
┌─────────────────────────┐
│       HomeLab OS        │  (Running Production Services: Postgres, Redis, Backend, Frontend)
└─────────────────────────┘
```

---

## 🔗 Pipeline Stage Specifications

1. **Stage 1: Developer Machine**: Features engineered locally. Docker optional. Automated tests verified via Pytest.
2. **Stage 2: Git Repository**: Pushed to `origin/main` after automated security scan (`scripts/security_scan.sh`) passes.
3. **Stage 3: Release Package**: Release artifacts produced and registered in `release/version.json` following SemVer.
4. **Stage 4: Installer Execution**: Triggered either via Windows Remote Installation Assistant or native Linux installer script.
5. **Stage 5: HomeLab Deployment Server**: Targeted deployment to Ubuntu 24.04 LTS on Dell Inspiron 5558.
6. **Stage 6: Docker Runtime**: Services initialized via Docker Compose with health checks and persistent storage.
