# HomeLab OS v1.0.0 — Production Deployment Guide

## 🚀 Prerequisites
- Docker v24.0+ & Docker Compose v2.20+
- Python 3.10+ (if running bare-metal)
- Ports 8000 (Backend API) and 3000/5173 (Frontend Dashboard) available

## 🐳 Docker Deployment Instructions
```bash
# Clone the repository
git clone https://github.com/SidddhantJain/HomeLab-OS.git
cd HomeLab-OS

# Run pre-flight requirement check
bash deployment/requirements_check.sh

# Build & launch production containers
docker compose up -d --build
```

Access Dashboard at `http://<server-ip>:3000` and API docs at `http://<server-ip>:8000/docs`.
