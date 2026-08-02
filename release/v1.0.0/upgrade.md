# HomeLab OS v1.0.0 Upgrade Guide

## Upgrading from Pre-Release Builds
```bash
git pull origin main
docker compose down
docker compose up -d --build
```
Automatic database migrations run on boot. No manual table migration required.
