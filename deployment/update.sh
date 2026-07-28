#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="/opt/homelab/backups/update_$(date +%Y%m%d_%H%M%S)"

echo "=========================================="
echo "       HomeLab OS System Updater          "
echo "=========================================="

echo "[Step 1/5] Backing Up Current Deployment..."
mkdir -p "$BACKUP_DIR"
if [ -f "$ROOT_DIR/.env" ]; then
    cp "$ROOT_DIR/.env" "$BACKUP_DIR/.env"
fi
echo "Backup saved to $BACKUP_DIR"

echo "[Step 2/5] Fetching Latest Release Code..."
cd "$ROOT_DIR"
if [ -d .git ]; then
    git fetch origin main
    git reset --hard origin/main
else
    echo "Notice: Not a git repository, skipping git pull."
fi

echo "[Step 3/5] Rebuilding & Restarting Services..."
docker compose down
docker compose up -d --build

echo "[Step 4/5] Running Post-Update Health Verification..."
sleep 5
if bash "$SCRIPT_DIR/health_check.sh"; then
    echo "=========================================="
    echo "SUCCESS: HomeLab OS update verified healthy!"
    echo "=========================================="
else
    echo "=========================================="
    echo "WARNING: Health check failed post-update!"
    echo "Rollback option available. Backup location: $BACKUP_DIR"
    read -p "Would you like to perform an immediate rollback? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Executing rollback..."
        if [ -f "$BACKUP_DIR/.env" ]; then
            cp "$BACKUP_DIR/.env" "$ROOT_DIR/.env"
        fi
        docker compose down
        docker compose up -d
        echo "Rollback completed."
    fi
fi
