HomeLab OS API Specification

API style:

REST API

JSON

JWT Authentication

Base URL:

http://homelab.local/api/v1
Authentication
Login
POST

/auth/login

Request:

{
"username":"admin",
"password":"password"
}

Response:

{
"token":"JWT_TOKEN"
}
User API
Get users
GET

/users
Create user
POST

/users
Dashboard API
System status
GET

/system/status

Response:

{
"cpu":20,
"ram":60,
"temperature":48,
"uptime":"12 days"
}
Storage API
List disks
GET

/storage/devices
Mount storage
POST

/storage/mount
Disk health
GET

/storage/health
Vault API
Vault status
GET

/vault/status

Response:

{
"status":"locked"
}
Unlock vault
POST

/vault/unlock
Lock vault
POST

/vault/lock
Workspace API
List workspace
GET

/workspaces
Start workspace
POST

/workspaces/{id}/start
Stop workspace
POST

/workspaces/{id}/stop
Project API
Create project
POST

/projects
Backup project
POST

/projects/{id}/backup
Create snapshot
POST

/projects/{id}/snapshot
Snapshot API
Policies
GET

/snapshots/policies
Update retention
PUT

/snapshots/policies/{id}

Example:

{
"keep_cycles":10
}
Maintenance API

Run maintenance:

POST

/system/maintenance

Response:

{
"status":"started"
}
Notification API

Get alerts:

GET

/notifications
