# Advanced Monitoring & Observability Architecture

## Overview
Monitors system hardware metrics via HAL, containers, database status, and historical telemetry recordings.

## Components
- **SystemMetricsCollector**: Gathers CPU, RAM, Disk, Temperature, Network, and Power state.
- **MetricsHistoryStore**: Database store for metric telemetry history.
- **ThresholdEvaluator**: Evaluates metrics against configurable thresholds.
- **Monitoring API**: `/api/v1/monitoring/status`, `/history`, `/services`, `/threshold`.
