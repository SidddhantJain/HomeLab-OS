# Intelligent Alert System Specification

## Overview
Evaluates operational thresholds and dispatches multi-severity alert notifications.

## Alert Severities
- `INFO`: Operational informative updates.
- `WARNING`: Early warning triggers (e.g. CPU > 80%).
- `CRITICAL`: High priority alerts (e.g. Disk > 90%).
- `EMERGENCY`: Immediate system threats (e.g. Thermal breach > 85°C).

## Notification Channels
- Email, Telegram Bot API, Webhooks, Browser Desktop Badges (`config/notifications.yml`).
