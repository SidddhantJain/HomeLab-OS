1. Database Purpose

The HomeLab OS database stores:

Users
Permissions
Projects
Workspaces
Services
Storage information
Backup policies
Snapshot policies
Notifications
Hardware monitoring data
System events
Configuration

The database does NOT store actual files.

Files remain in:

SSD
External HDD
Encrypted Vault

The database stores metadata and control information.

2. Entity Relationship Overview
                    USERS
                      |
                      |
                 USER_ROLES
                      |
                      |
       ┌──────────────┼───────────────┐
       |              |               |
    PROJECTS     WORKSPACES       VAULTS
       |              |               |
       |              |               |
 BACKUP_POLICY   SERVICES       ACCESS_LOGS
       |
 SNAPSHOTS
       |
 FILE_VERSIONS


SYSTEM
 |
 ├── HARDWARE_STATUS
 |
 ├── NOTIFICATIONS
 |
 └── AUDIT_LOGS
3. Tables
3.1 Users Table

Stores system users.

users
Column	Type	Description
id	UUID	Primary key
username	VARCHAR	Login name
email	VARCHAR	Email
password_hash	TEXT	Encrypted password
status	ENUM	Active/Disabled
created_at	TIMESTAMP	Creation time
last_login	TIMESTAMP	Last login

Example:

admin
developer
viewer
3.2 Roles Table
roles
Column	Type
id	UUID
name	VARCHAR
permissions	JSON

Example:

{
 "docker":true,
 "storage":true,
 "vault":false
}
3.3 User Roles

Many-to-many mapping.

user_roles
Column
user_id
role_id
3.4 Projects Table

Stores development projects.

projects

Fields:

Column	Type
id	UUID
name	VARCHAR
description	TEXT
language	VARCHAR
framework	VARCHAR
path	TEXT
git_repo	TEXT
status	ENUM
created_at	TIMESTAMP

Example:

Fake News Detection

Language:
Python

Framework:
PyTorch
3.5 Workspaces Table

Development environments.

workspaces
Column	Type
id	UUID
name	VARCHAR
profile	ENUM
config	JSON
status	ENUM

Example:

{
"docker":["postgres","redis"],
"memory_limit":"2GB"
}
3.6 Workspace Services

Links containers to workspaces.

workspace_services
Column
workspace_id
service_name
container_id

Example:

Developer Workspace

- PostgreSQL
- Redis
- Node
3.7 Storage Devices

Tracks disks.

storage_devices
Column
id
name
mount_point
filesystem
capacity
free_space
health
type

Example:

External HDD

/dev/sdb

1TB

ext4
3.8 Storage Locations

Folders.

storage_locations
Column
id
device_id
path
purpose

Example:

/mnt/storage/projects

purpose:
Projects
3.9 Vaults

Encrypted storage.

vaults
Column
id
name
size
encryption
mount_point
status
created_at

Example:

Private Vault

100GB

LUKS

Locked
3.10 Snapshot Policies

Controls deletion rules.

snapshot_policies

Fields:

Column
id
project_id
frequency
retention_count
max_storage
auto_delete

Example:

{
"cycle":10,
"weekly":8,
"monthly":12
}
3.11 Snapshots

Actual snapshot records.

snapshots
Column
id
project_id
created_at
size
location
status
3.12 File Versions

Tracks versions.

file_versions
Column
id
file_path
version
created_at
checksum
3.13 Backup Jobs
backup_jobs
Column
id
source
destination
schedule
status
3.14 Notifications
notifications
Column
id
type
message
severity
timestamp
read

Example:

WARNING

External HDD temperature high
3.15 Hardware Monitoring
hardware_metrics

Stores:

CPU temperature
RAM usage
Disk health
Network
3.16 Audit Logs

Important for security.

audit_logs

Example:

2026-07-28

admin unlocked vault

192.168.1.10