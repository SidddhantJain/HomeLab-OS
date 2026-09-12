#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "      🖥️ HomeLab OS PySide6 Desktop Manager Console       "
echo "=========================================================="
echo "Launching Native Desktop Management Interface..."
echo "=========================================================="

python3 manager/main.py
