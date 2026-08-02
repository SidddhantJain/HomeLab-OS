# HomeLab OS v1.0.0 Installation Guide

## Quick Start (Docker Compose)
```bash
# 1. Clone repository
git clone https://github.com/SidddhantJain/HomeLab-OS.git
cd HomeLab-OS

# 2. Run system requirements check
bash deployment/requirements_check.sh

# 3. Deploy container stack
bash deployment/install.sh
```

Access the dashboard at `http://<server-ip>:3000` and API at `http://<server-ip>:8000/api/v1/system/status`.
