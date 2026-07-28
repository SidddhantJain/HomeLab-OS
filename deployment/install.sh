#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "    HomeLab OS Production Deployment      "
echo "=========================================="

echo "[Step 1/5] Verifying System Requirements..."
bash "$SCRIPT_DIR/requirements_check.sh"

echo "[Step 2/5] Creating System Directories..."
sudo mkdir -p /opt/homelab /var/log/homelab /mnt/storage /mnt/vault
sudo chmod 755 /opt/homelab /var/log/homelab

echo "[Step 3/5] Provisioning Environment Configuration..."
if [ ! -f "$ROOT_DIR/.env" ]; then
    echo "Creating .env from template..."
    cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
    
    # Generate random secret key if openssl is available
    if command -v openssl >/dev/null 2>&1; then
        RAND_SECRET=$(openssl rand -hex 32)
        sed -i.bak "s/SECRET_KEY=.*/SECRET_KEY=$RAND_SECRET/" "$ROOT_DIR/.env" rm -f "$ROOT_DIR/.env.bak"
    fi
fi

echo "[Step 4/5] Building & Launching Container Services..."
cd "$ROOT_DIR"
docker compose up -d --build

echo "[Step 5/5] Performing Initial Health Verification..."
sleep 5
bash "$SCRIPT_DIR/health_check.sh"

echo "=========================================="
echo "HomeLab OS Production Deployment Complete!"
echo "Dashboard URL: http://localhost:3000"
echo "API Endpoint:  http://localhost:8000/api/v1/system/status"
echo "=========================================="
