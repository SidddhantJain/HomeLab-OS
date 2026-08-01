# Health Center & Score Engine Specification

## Overview
Aggregates server health indicators (CPU load, RAM usage, SMART warnings, network latency) to calculate a 0-100 Health Score.

## Endpoints
- `GET /api/v1/health/summary`: Returns overall Health Score and component metrics.
