
Development Environment Setup

Development Machine

Recommended:

Your main laptop.

Not the server.

Required Software
Git

Install:

sudo apt install git
Python

Version:

Python 3.12+

Install:

sudo apt install python3 python3-pip python3-venv
Node.js

Required for frontend.

Recommended:

Node.js LTS
Docker

Development environment:

sudo apt install docker.io docker-compose
PostgreSQL

For local development:

sudo apt install postgresql
Backend Environment

Create:

backend/.venv

Activate:

source .venv/bin/activate

Install:

fastapi
uvicorn
sqlalchemy
psycopg2
pydantic
python-jose
passlib
Frontend Environment

Install:

npm install

Packages:

react
react-router
axios
tailwind
chart.js
Development Database

Local:

PostgreSQL

Database:

homelab_dev
Development Workflow
Feature Development

Example:

New Snapshot Feature

Create branch

↓

feature/snapshot-engine

↓

Backend API

↓

Database migration

↓

Frontend UI

↓

Tests

↓

Merge
Git Branch Model
main
 |
 |
develop
 |
 |
feature/*
Coding Standards

Backend:

PEP8
Type hints
Docstrings
Unit tests

Frontend:

ESLint
Component-based
Reusable UI
Local Testing

Before deployment:

Developer Laptop

↓

Docker Compose

↓

Test Environment

↓

Server Deployment
CI/CD Future

Later:

Git Push

↓

Tests

↓

Build Docker Image

↓

Deploy to HomeLab Server
Development Milestone
Milestone 1

Foundation

Deliver:

✅ FastAPI backend
✅ React dashboard
✅ Authentication
✅ PostgreSQL integration

Milestone 2

Storage Layer

Deliver:

✅ Storage manager
✅ Vault manager
✅ Backup engine

Milestone 3

Developer Platform

Deliver:

✅ Workspace manager
✅ Project manager
✅ Docker control

Milestone 4

Automation

Deliver:

✅ Snapshot engine
✅ Scheduler
✅ Maintenance center
✅ Power manager