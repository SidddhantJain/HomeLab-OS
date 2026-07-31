# Snapshot Service Architecture

## Purpose
Manages point-in-time filesystem state captures and enforces limits on retention cycles.

## Components
1. **SnapshotManager**: Generates system snapshots and prunes older records beyond limits.
2. **Retention Policy**: Keeps a maximum number of historical snapshots (default = 10).
