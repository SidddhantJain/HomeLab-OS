#!/usr/bin/env bash
set -eo pipefail

echo "=========================================="
echo "    HomeLab OS Server Health Monitor      "
echo "=========================================="

FAILED=0

# 1. Docker Status
echo -n "[1/5] Checking Docker Daemon... "
if docker info >/dev/null 2>&1; then
    echo "OK (Running)"
else
    echo "FAILED (Daemon unavailable)"
    FAILED=1
fi

# 2. Container Status
echo "[2/5] Checking Container Health..."
for CONTAINER in homelab_postgres homelab_redis homelab_backend homelab_frontend; do
    if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null)" == "true" ]; then
        echo "  - $CONTAINER: RUNNING"
    else
        echo "  - $CONTAINER: STOPPED or MISSING"
        FAILED=1
    fi
done

# 3. API Availability
echo -n "[3/5] Checking FastAPI Core API... "
API_RES=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:8000/ || echo "000")
if [ "$API_RES" -eq 200 ]; then
    echo "OK (HTTP 200)"
else
    echo "FAILED (HTTP $API_RES)"
    FAILED=1
fi

# 4. Database Availability
echo -n "[4/5] Checking PostgreSQL Database... "
if docker exec homelab_postgres pg_isready -U homelab -d homelab_db >/dev/null 2>&1; then
    echo "OK (Accepting connections)"
else
    echo "FAILED (Database connection error)"
    FAILED=1
fi

# 5. Storage Mount Availability
echo -n "[5/5] Checking Storage Mount Point... "
if [ -d /mnt/storage ]; then
    echo "OK (/mnt/storage present)"
else
    echo "WARNING (/mnt/storage missing)"
fi

echo "=========================================="
if [ "$FAILED" -eq 0 ]; then
    echo "STATUS: ALL SYSTEMS HEALTHY & OPERATIONAL"
    exit 0
else
    echo "STATUS: HEALTH CHECK DETECTED DEGRADED SERVICES"
    exit 1
fi
