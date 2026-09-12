#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "      🏠 HomeLab OS Server Engine (FastAPI Backend)       "
echo "=========================================================="
echo "Starting HomeLab OS Server on http://localhost:8000 ..."
echo "Press Ctrl+C at any time to stop the server."
echo "=========================================================="

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
