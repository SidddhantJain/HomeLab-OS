import os
import subprocess
import socket
import psutil
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/services", tags=["Hosted Services Management"])

SERVICES_DEFINITIONS = [
    {
        "id": "homelab-frontend",
        "name": "HomeLab OS Web Frontend",
        "description": "Core React/Vite web interface and system management dashboard.",
        "port": 5173,
        "virtual_ip": "192.168.0.182",
        "url": "http://192.168.0.182:5173",
        "vip_url": "http://192.168.0.182/",
        "type": "frontend",
        "category": "Core Platform",
        "process_pattern": "serve_spa.py",
        "start_cmd": "nohup python3 /home/server/HomeLab-OS/frontend/serve_spa.py 5173 >/home/server/homelab_frontend.log 2>&1 &",
        "stop_cmd": "pkill -9 -f 'serve_spa.py' || pkill -9 -f '5173' || true"
    },
    {
        "id": "homelab-backend",
        "name": "HomeLab OS Core API Engine",
        "description": "FastAPI high-performance server core backend.",
        "port": 8000,
        "virtual_ip": "192.168.0.182",
        "url": "http://192.168.0.182:8000/docs",
        "vip_url": "http://192.168.0.182:8000/",
        "type": "backend",
        "category": "Core Platform",
        "process_pattern": "port 8000",
        "start_cmd": "nohup /home/server/HomeLab-OS/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/HomeLab-OS/backend --host 0.0.0.0 --port 8000 >/home/server/homelab_backend.log 2>&1 &",
        "stop_cmd": "pkill -9 -f 'port 8000' || true"
    },
    {
        "id": "madenmore-store",
        "name": "MadeNMore 3D Print Store & Inventory",
        "description": "Express REST API backend & high-speed SPA with dynamic JSON persistence.",
        "port": 5174,
        "api_port": 4000,
        "virtual_ip": "192.168.0.186 / 192.168.0.183",
        "url": "http://192.168.0.182:5174",
        "vip_url": "http://192.168.0.186/",
        "type": "fullstack",
        "category": "Production Apps",
        "process_pattern": "server/api.js",
        "start_cmd": "cd /home/server/apps/MadeNMore && nohup env PORT=5174 node server/api.js >/home/server/madenmore.log 2>&1 & nohup env PORT=4000 node server/api.js >/home/server/madenmore_api.log 2>&1 &",
        "stop_cmd": "pkill -9 -f 'node server/api.js' || true"
    },
    {
        "id": "fiscalflow",
        "name": "FiscalFlow Wealth Intelligence",
        "description": "Enterprise financial analytics, portfolio balancing and ledger platform.",
        "port": 8081,
        "virtual_ip": "192.168.0.184",
        "url": "http://192.168.0.182:8081/docs",
        "vip_url": "http://192.168.0.184/",
        "type": "backend",
        "category": "Production Apps",
        "process_pattern": "FiscalFlow",
        "start_cmd": "nohup /home/server/apps/FiscalFlow/backend/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/apps/FiscalFlow/backend --host 0.0.0.0 --port 8081 >/home/server/fiscal.log 2>&1 &",
        "stop_cmd": "pkill -9 -f 'FiscalFlow' || true"
    },
    {
        "id": "madenmore-studio",
        "name": "MadeNMore 3D Creative Studio",
        "description": "Next.js 16 & React 19 web application with 3D Studio, Alps, CRM, and ERP.",
        "port": 5175,
        "virtual_ip": "192.168.0.185",
        "url": "http://192.168.0.182:5175",
        "vip_url": "http://192.168.0.185/",
        "type": "fullstack",
        "category": "Production Apps",
        "process_pattern": "5175",
        "start_cmd": "cd /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_creative_studio && nohup npx next start -p 5175 -H 0.0.0.0 >/home/server/stitch3d.log 2>&1 &",
        "stop_cmd": "pkill -9 -f 'next start -p 5175' || true; pkill -9 -f 'next-server' || true"
    },
    {
        "id": "nginx-vips",
        "name": "Nginx & Virtual IP Aliases",
        "description": "IP alias routing (192.168.0.182-187) and reverse proxy routing on port 80.",
        "port": 80,
        "virtual_ip": "192.168.0.182-187",
        "url": "http://192.168.0.182/",
        "vip_url": "http://192.168.0.182/",
        "type": "infrastructure",
        "category": "Infrastructure",
        "process_pattern": "nginx",
        "start_cmd": "bash /home/server/setup_virtual_ips.sh; echo 1 | sudo -S systemctl restart nginx || true",
        "stop_cmd": "echo 1 | sudo -S systemctl stop nginx || true"
    }
]

def check_port_open(port: int, host: str = "127.0.0.1") -> bool:
    hosts_to_try = [host, "127.0.0.1", "192.168.0.182", "0.0.0.0"]
    for h in hosts_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.4)
                if s.connect_ex((h, port)) == 0:
                    return True
        except Exception:
            pass
    return False

def get_process_info_for_port(port: int, pattern: str = "") -> Dict[str, Any]:
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
                if conn.pid:
                    try:
                        p = psutil.Process(conn.pid)
                        return {
                            "pid": conn.pid,
                            "cpu_percent": round(p.cpu_percent(interval=0.05), 1),
                            "memory_mb": round(p.memory_info().rss / (1024 * 1024), 1),
                            "status": "RUNNING"
                        }
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        return {"pid": conn.pid, "cpu_percent": 0.0, "memory_mb": 0.0, "status": "RUNNING"}
    except Exception:
        pass
    
    if pattern:
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmd_line = ' '.join(p.info['cmdline'] or [])
                if pattern in cmd_line or pattern == p.info['name']:
                    return {
                        "pid": p.info['pid'],
                        "cpu_percent": 0.1,
                        "memory_mb": round(p.memory_info().rss / (1024 * 1024), 1),
                        "status": "RUNNING"
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    is_open = check_port_open(port)
    if is_open:
        return {"pid": None, "cpu_percent": 0.0, "memory_mb": 0.0, "status": "RUNNING"}
    return {"pid": None, "cpu_percent": 0.0, "memory_mb": 0.0, "status": "STOPPED"}


@router.get("/list")
def list_hosted_services():
    services_status = []
    for s_def in SERVICES_DEFINITIONS:
        proc_info = get_process_info_for_port(s_def["port"], s_def.get("process_pattern", ""))
        service_data = {
            **s_def,
            "is_running": proc_info["status"] == "RUNNING",
            "pid": proc_info["pid"],
            "cpu_percent": proc_info["cpu_percent"],
            "memory_mb": proc_info["memory_mb"],
            "status_text": "ONLINE" if proc_info["status"] == "RUNNING" else "OFFLINE"
        }
        services_status.append(service_data)
    
    return {
        "services": services_status,
        "total": len(services_status),
        "running_count": sum(1 for s in services_status if s["is_running"]),
        "server_ip": "192.168.0.182"
    }


@router.post("/start/{service_id}")
def start_service(service_id: str):
    target = next((s for s in SERVICES_DEFINITIONS if s["id"] == service_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Service definition not found")
    
    try:
        subprocess.Popen(target["start_cmd"], shell=True, executable="/bin/bash")
        return {"status": "success", "message": f"Service '{target['name']}' started successfully.", "service_id": service_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start service: {str(e)}")


@router.post("/stop/{service_id}")
def stop_service(service_id: str):
    target = next((s for s in SERVICES_DEFINITIONS if s["id"] == service_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Service definition not found")
    
    try:
        subprocess.run(target["stop_cmd"], shell=True, executable="/bin/bash")
        return {"status": "success", "message": f"Service '{target['name']}' stopped successfully.", "service_id": service_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop service: {str(e)}")


@router.post("/restart/{service_id}")
def restart_service(service_id: str):
    target = next((s for s in SERVICES_DEFINITIONS if s["id"] == service_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Service definition not found")
    
    try:
        subprocess.run(target["stop_cmd"], shell=True, executable="/bin/bash")
        subprocess.Popen(target["start_cmd"], shell=True, executable="/bin/bash")
        return {"status": "success", "message": f"Service '{target['name']}' restarted.", "service_id": service_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart service: {str(e)}")


@router.post("/restart-all")
def restart_all_services():
    try:
        subprocess.Popen("bash /home/server/start_web_services.sh", shell=True, executable="/bin/bash")
        return {"status": "success", "message": "All HomeLab OS hosted services and Virtual IPs restarted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart all services: {str(e)}")
