# Backup Service Architecture

## Purpose
Orchestrates automated and manual folder synchronization between workspaces and external disks or networks.

## Components
1. **BackupManager**: Spawns copy operations, records logs, and updates DB statuses.
2. **BackupScheduler**: Registers backup schedules with the global scheduler engine.
