# HomeLab OS v1.0.0 — Developer Guide

## Local Development Setup

### 1. Backend Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

### 3. Running Test Suites
```bash
python -m pytest tests/backend -v
bash scripts/security_scan.sh
```
