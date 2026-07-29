# Scheduler Framework Design

## Purpose

The Scheduler framework provides a single, lifecycle-aware scheduling coordinator for HomeLab OS. It replaces ad-hoc loops or multiple OS cron schedules with a unified system that handles storage snapshots, automated backups, health check polling, and telemetry reports.

## Scope

- Schedules jobs using interval, cron, or one-shot time models.
- Integrates with the Server State Machine to pause/resume jobs based on system state.
- Supports cancel, register, list, and disable APIs.

## State Lifecycle Integration

Certain high-load or locking server transitions require cron tasks to pause to prevent data corruption.
When the [ServerStateMachine](file:///d:/Siddhant/projects/HomeLab%20OS/backend/app/core/server_state.py) transitions to:
- `MAINTENANCE`
- `BACKUP`
- `UPDATING`
- `RESTORING`
- `SHUTTING_DOWN`

The scheduler automatically pauses its execution runner. Active cron hooks are cached and will only run again once the server is back in the `RUNNING` state.

## Job Registration Model

```python
from app.core.scheduler import Scheduler, ScheduleMode

scheduler = Scheduler()

# Register interval execution
scheduler.register(
    name="Disk Health Scan",
    service="storage",
    mode=ScheduleMode.INTERVAL,
    interval_seconds=3600,
    callback=run_disk_smart_check
)
```
