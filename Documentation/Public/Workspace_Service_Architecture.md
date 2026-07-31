# Workspace Service Architecture

## Purpose
The Workspace Service manages developer workspace allocations, computes usage metrics, and coordinates lifecycle events.

## Components
1. **WorkspaceManager**: Computes sizes recursively, registers folders, and handles cloning operations.
2. **WorkspaceService**: Implements API mappings and dispatches events.

## State Transitions
```
ACTIVE ──► ARCHIVED ──► ACTIVE
  │
  ▼
DELETED
```
- **ACTIVE**: Root storage path exists and is operational.
- **ARCHIVED**: Config archive mapped.
- **DELETED**: Mark status to skip directory scan.
