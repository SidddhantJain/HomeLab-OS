Phase 1 Development Environment Bootstrap

Now we prepare the actual development environment for building HomeLab OS.

Phase 1 Goal

At the end:

You should have:

Developer Laptop

        |
        |
Git Repository

        |
        |
Docker Development Environment

        |
        |
HomeLab Server Deployment
1. Development Machine

Recommended:

Your main laptop.

Not the Dell server.

Reason:

Faster development
Easier debugging
Server remains stable
2. Repository Creation

Create:

homelab-os

Structure:

homelab-os/

├── backend
├── frontend
├── database
├── docker
├── scripts
├── docs
└── tests
3. Initialize Git
git init

Create:

.gitignore

Example:

.env

__pycache__

node_modules

*.log

database/*.db
4. Backend Bootstrap

Create environment:

mkdir backend

cd backend

python3 -m venv venv

Activate:

source venv/bin/activate

Install:

pip install \
fastapi \
uvicorn \
sqlalchemy \
psycopg2-binary \
python-jose \
passlib \
bcrypt \
python-dotenv

Create:

backend/

├── app/
│
├── main.py
├── requirements.txt
└── .env
5. First FastAPI Test

main.py:

from fastapi import FastAPI

app = FastAPI(
    title="HomeLab OS API"
)


@app.get("/")
def home():
    return {
        "status":"running",
        "system":"HomeLab OS"
    }

Run:

uvicorn main:app --reload

Test:

http://localhost:8000

Expected:

{
"status":"running",
"system":"HomeLab OS"
}
6. Frontend Bootstrap

Create:

npm create vite@latest frontend

Select:

React
JavaScript

Install:

cd frontend

npm install

Install:

npm install axios react-router-dom

Run:

npm run dev
7. Database Bootstrap

Install PostgreSQL:

sudo apt install postgresql

Create:

CREATE DATABASE homelab;

Create user:

CREATE USER homelab_admin
WITH PASSWORD 'strong_password';

Grant:

GRANT ALL PRIVILEGES
ON DATABASE homelab
TO homelab_admin;
8. Docker Development Setup

Create:

docker/

├── docker-compose.yml

Initial:

services:

 postgres:
   image: postgres:16
   environment:
    POSTGRES_DB: homelab
    POSTGRES_USER: homelab
    POSTGRES_PASSWORD: password

   ports:
    - "5432:5432"


 redis:
   image: redis:latest

   ports:
    - "6379:6379"

Run:

docker compose up -d
9. Environment Variables

Never hardcode passwords.

Create:

.env

Example:

DATABASE_URL=
POSTGRES_PASSWORD=
SECRET_KEY=
10. Development Workflow

Daily:

Start Coding

↓

Run Docker Services

↓

Backend Development

↓

Frontend Development

↓

Tests

↓

Git Commit

↓

Push

11. First Development Milestone
Milestone 1A — Core Skeleton

Deliver:

✅ Repository
✅ FastAPI backend
✅ React dashboard
✅ PostgreSQL connection
✅ Docker environment
✅ Login page

Milestone 1B — System API

Add:

/system/status

Returns:

{
"cpu":20,
"ram":50,
"disk":70
}
Milestone 1C — First Dashboard

Display:

CPU
RAM
Storage
Server Status
Phase 1 Completion Criteria

Before moving forward:

☑ Backend running
☑ Frontend running
☑ Database connected
☑ Docker working
☑ Git workflow established
☑ Server can pull code