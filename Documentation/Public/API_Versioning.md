# API Stability & Versioning Strategy

## Router Versioning Strategy
- `/api/v1/`: Stable production endpoints maintaining backward compatibility across HomeLab OS v1 releases.
- `/api/v2/`: Forward-looking experimental API versioning gateway (`GET /api/v2/status`).

## Deprecation Policy
No `/api/v1/` endpoint will be removed without a minimum of 2 minor release cycles of deprecation notices.
