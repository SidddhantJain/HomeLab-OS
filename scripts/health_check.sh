#!/usr/bin/env bash
set -eo pipefail

echo "=========================================="
echo "      HomeLab OS Health Check Script      "
echo "=========================================="

echo "[1/4] Checking Backend API Root..."
curl -s http://localhost:8000/ | grep '"status":"running"' && echo " -> Backend API OK" || echo " -> Backend API Failed"

echo "[2/4] Checking System Status Endpoint..."
curl -s http://localhost:8000/api/v1/system/status | grep '"status":"running"' && echo " -> System Status API OK" || echo " -> System Status API Failed"

echo "[3/4] Checking PostgreSQL Docker Container..."
docker compose ps postgres | grep "healthy" && echo " -> PostgreSQL OK" || echo " -> PostgreSQL Not Healthy"

echo "[4/4] Checking Redis Docker Container..."
docker compose ps redis | grep "healthy" && echo " -> Redis OK" || echo " -> Redis Not Healthy"

echo "=========================================="
echo "Health Check Complete."
