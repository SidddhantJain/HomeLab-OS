. Docker Philosophy

HomeLab OS will follow a container-first architecture.

The rule:

Every major service should run independently, be replaceable, upgradeable, and recoverable.

Instead of:

Ubuntu
 |
 ├── Installed Software
 ├── Dependencies
 ├── Configurations
 └── Conflicts

We use:

Ubuntu Host

 |
 Docker Engine

 |
 ├── Container A
 ├── Container B
 ├── Container C

Advantages:

Easy updates.
Isolation.
Backup simplicity.
Migration to new hardware.
Less dependency conflicts.
2. Overall Docker Architecture
                    HomeLab OS

                         |
                         |
                  Docker Engine

                         |
 ┌───────────────────────┼────────────────────────┐
 |                       |                        |
Core Services       Development Services     Management
 |                       |                        |
 |                       |                        |
Backend API          Gitea                  Monitoring
Frontend             Databases              Notifications
Database             Redis                  Dashboard
3. Container Groups

HomeLab OS will separate containers into stacks.

Stack 1: Core Platform

Purpose:

The brain of HomeLab OS.

homelab-core

Contains:

├── Backend API
├── Frontend Dashboard
├── PostgreSQL
└── Redis
Backend Container

Name:

homelab-api

Technology:

FastAPI
Python

Responsibilities:

Authentication.
API routing.
Service communication.
User management.
Automation control.

Ports:

8000
Frontend Container

Name:

homelab-dashboard

Technology:

React
Nginx

Port:

80
PostgreSQL

Name:

homelab-db

Stores:

Users.
Projects.
Configurations.
Logs.
Policies.
Redis

Name:

homelab-cache

Used for:

Sessions.
Background jobs.
Task queues.
Stack 2: Development Platform

Purpose:

Developer environment.

homelab-development
Gitea

Container:

gitea

Purpose:

Private GitHub alternative.

Stores:

Source code.
Issues.
Documentation.
PostgreSQL Databases

Separate from HomeLab OS database.

Example:

developer-postgres

For:

Projects.
Applications.
Testing.
Redis

For development applications.

Stack 3: Storage Services
homelab-storage
Samba

Container:

samba

Provides:

Windows access:

\\homelab\storage

Folders:

Projects
Research
Shared
Downloads
Syncthing

Container:

syncthing

Purpose:

Automatic synchronization.

Examples:

Laptop
 |
 |
HomeLab
 |
 |
Backup
Stack 4: Backup System
homelab-backup

Components:

Backup Engine

Handles:

Scheduled backups.
Compression.
Verification.
Snapshot Engine

Handles:

Project snapshots.
Retention rules.
Cleanup.

Example:

Project

 |
 Snapshot

 |
 Cycle 1
 Cycle 2
 Cycle 3

 |
 Delete old based on policy
Stack 5: Monitoring
homelab-monitoring
Prometheus

Collects:

CPU.
RAM.
Disk.
Network.
Grafana

Displays:

Dashboard:

CPU
RAM
Temperature
Disk Health
Network
Uptime Kuma

Monitors:

Containers.
Websites.
APIs.
Stack 6: Documentation
homelab-docs

Possible technology:

Wiki.js

or

BookStack

Purpose:

Personal knowledge base.

Stack 7: Download Manager
homelab-download

Components:

Example:

qBittorrent
aria2

Features:

Queue.
Scheduling.
Storage selection.
Stack 8: Reverse Proxy

Important.

Container:

caddy

Purpose:

Single entry point.

Example:

Instead of:

192.168.1.20:8000
192.168.1.20:3000
192.168.1.20:9090

You use:

dashboard.home
git.home
docs.home
monitor.home
Final Docker Layout
Docker

|
├── Core
│   ├── API
│   ├── Dashboard
│   ├── PostgreSQL
│   └── Redis
│
├── Development
│   ├── Gitea
│   ├── PostgreSQL
│   └── Redis
│
├── Storage
│   ├── Samba
│   └── Syncthing
│
├── Automation
│   ├── Scheduler
│   ├── Backup
│   └── Snapshot
│
├── Monitoring
│   ├── Prometheus
│   ├── Grafana
│   └── Uptime Kuma
│
├── Documentation
│   └── Wiki
│
└── Networking
    └── Caddy
Resource Planning (Important for your 8GB RAM)

Your laptop:

8GB RAM
i7-5500U

We cannot run everything at maximum.

Initial memory target:

Service	RAM
Ubuntu	1.5GB
HomeLab API	300MB
Dashboard	100MB
PostgreSQL	500MB
Redis	100MB
Gitea	300MB
Monitoring	500MB
Docker overhead	500MB

Approx:

4GB-5GB

Leaves:

3GB

for development workloads.

Important optimization

Not all services should run permanently.

This connects with your Workspace Manager.

Example:

Normal mode:

Core
Monitoring
Storage

Running.

Developer mode:

+
Gitea
+
Database
+
Redis
+
Project Containers

Research mode:

+
Python
+
Jupyter
+
ML tools