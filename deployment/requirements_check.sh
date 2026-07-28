#!/usr/bin/env bash
set -eo pipefail

echo "=========================================="
echo " HomeLab OS - Deployment Requirements Check"
echo "=========================================="

FAILED=0

# 1. Verify OS (Target: Ubuntu 24.04 LTS or compatible Linux distribution)
echo -n "[1/5] Checking Operating System... "
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "$NAME $VERSION_ID"
    if [[ "$ID" != "ubuntu" ]]; then
        echo " -> WARNING: Recommended OS is Ubuntu 24.04 LTS (Detected: $NAME)."
    fi
else
    echo " -> Unable to determine OS (/etc/os-release missing)."
    FAILED=1
fi

# 2. Verify Docker availability
echo -n "[2/5] Checking Docker Engine... "
if command -v docker >/dev/null 2>&1; then
    DOCKER_VER=$(docker --version)
    echo "OK ($DOCKER_VER)"
else
    echo "FAILED! Docker is mandatory on the deployment server."
    FAILED=1
fi

# 3. Verify Docker Compose availability
echo -n "[3/5] Checking Docker Compose... "
if docker compose version >/dev/null 2>&1; then
    COMPOSE_VER=$(docker compose version)
    echo "OK ($COMPOSE_VER)"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_VER=$(docker-compose --version)
    echo "OK ($COMPOSE_VER)"
else
    echo "FAILED! Docker Compose is mandatory on the deployment server."
    FAILED=1
fi

# 4. Check available RAM (Recommended >= 2000 MB for baseline services)
echo -n "[4/5] Checking Available Memory... "
if command -v free >/dev/null 2>&1; then
    TOTAL_RAM_MB=$(free -m | awk '/^Mem:/{print $2}')
    echo "${TOTAL_RAM_MB} MB"
    if [ "$TOTAL_RAM_MB" -lt 1800 ]; then
        echo " -> WARNING: Low RAM detected (${TOTAL_RAM_MB}MB). Recommended minimum is 2000MB."
    fi
else
    echo "Unable to measure memory (free utility not available)."
fi

# 5. Check Disk Space (Recommended >= 10GB free space)
echo -n "[5/5] Checking Storage Disk Space... "
FREE_DISK_GB=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
echo "${FREE_DISK_GB} GB free on /"
if [ "$FREE_DISK_GB" -lt 5 ]; then
    echo " -> FAILED: Insufficient disk space (${FREE_DISK_GB}GB free). Minimum 5GB required."
    FAILED=1
fi

echo "=========================================="
if [ "$FAILED" -eq 0 ]; then
    echo "SUCCESS: All deployment server prerequisites met!"
    exit 0
else
    echo "ERROR: Server requirements check failed. Please resolve issues above before installation."
    exit 1
fi
