#!/usr/bin/env bash
set -eo pipefail

echo "=========================================="
echo "    HomeLab OS Bootstrap & Deployment     "
echo "=========================================="

if [ ! -f .env ]; then
    echo "Creating .env configuration from template..."
    cp .env.example .env
fi

echo "Starting HomeLab OS container stack with Docker Compose..."
docker compose up -d --build

echo "Waiting for services to become healthy..."
sleep 10

echo "Deployment complete! Access Dashboard at http://localhost:3000"
