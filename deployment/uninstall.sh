#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

PURGE_DATA=0

if [[ "$1" == "--purge" ]]; then
    PURGE_DATA=1
fi

echo "=========================================="
echo "      HomeLab OS System Uninstaller       "
echo "=========================================="

echo "[1/3] Stopping & Removing Containers..."
cd "$ROOT_DIR"
if [ "$PURGE_DATA" -eq 1 ]; then
    echo "WARNING: Purge flag detected. User data volumes WILL be deleted!"
    docker compose down -v --rmi all
else
    echo "Preserving user data volumes (postgres_data, redis_data)..."
    docker compose down --rmi local
fi

echo "[2/3] Cleaning Transient Artifacts..."
rm -rf "$ROOT_DIR/backend/__pycache__" "$ROOT_DIR/frontend/dist"

if [ "$PURGE_DATA" -eq 1 ]; then
    echo "[3/3] Purging Environment Files..."
    rm -f "$ROOT_DIR/.env"
else
    echo "[3/3] User configuration (.env) preserved."
fi

echo "=========================================="
echo "Uninstallation complete."
if [ "$PURGE_DATA" -eq 0 ]; then
    echo "Notice: Persistent database volumes and configuration files were preserved."
    echo "Run with --purge to remove all data permanently."
fi
echo "=========================================="
