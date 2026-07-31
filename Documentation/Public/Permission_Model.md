# Role-Based Access Control (RBAC) Permission Model

## Purpose
Ensures strict user authentication and validates operations across platform boundaries.

## Architecture
- **System Roles**: `ADMIN`, `DEVELOPER`, `USER`, `GUEST`
- **Actions**: `READ`, `WRITE`, `DELETE`, `MOUNT`, `UNMOUNT`, `BACKUP`, `RESTORE`
- **Resources**: `storage`, `vault`, `workspace`, `projects`

## Policies
- **Admin**: Full access.
- **Developer**: Can read/write workspaces and projects.
- **Guest**: Read-only on storage.
