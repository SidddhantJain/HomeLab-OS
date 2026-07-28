#!/usr/bin/env bash
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=========================================="
echo "   HomeLab OS Native Linux Installer      "
echo "=========================================="

echo "Delegating installation to deployment core..."
bash "$ROOT_DIR/deployment/install.sh"
