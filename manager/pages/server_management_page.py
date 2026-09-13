import webbrowser
import paramiko
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, 
    QGridLayout, QScrollArea, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer


SERVICES_INFO = [
    {
        "id": "homelab-frontend",
        "name": "HomeLab OS Web Frontend",
        "desc": "React/Vite production web management console",
        "port": 5173,
        "vip": "192.168.0.182",
        "url": "http://192.168.0.182:5173",
        "vip_url": "http://192.168.0.182/",
        "pattern": "http.server 5173",
        "start": "nohup python3 -m http.server 5173 --bind 0.0.0.0 --directory /home/server/HomeLab-OS/frontend/dist >/home/server/homelab_frontend.log 2>&1 &",
        "stop": "pkill -9 -f 'http.server 5173' || true"
    },
    {
        "id": "homelab-backend",
        "name": "HomeLab OS Core API",
        "desc": "FastAPI high-speed system management backend engine",
        "port": 8000,
        "vip": "192.168.0.182",
        "url": "http://192.168.0.182:8000/docs",
        "vip_url": "http://192.168.0.182:8000/",
        "pattern": "port 8000",
        "start": "nohup /home/server/HomeLab-OS/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/HomeLab-OS/backend --host 0.0.0.0 --port 8000 >/home/server/homelab_backend.log 2>&1 &",
        "stop": "pkill -9 -f 'port 8000' || true"
    },
    {
        "id": "madenmore-store",
        "name": "MadeNMore 3D Print Store",
        "desc": "Express REST API & Store SPA with live JSON persistence",
        "port": 5174,
        "vip": "192.168.0.183",
        "url": "http://192.168.0.182:5174",
        "vip_url": "http://192.168.0.183/",
        "pattern": "server/api.js",
        "start": "cd /home/server/apps/MadeNMore && nohup env PORT=5174 node server/api.js >/home/server/madenmore.log 2>&1 & nohup env PORT=4000 node server/api.js >/home/server/madenmore_api.log 2>&1 &",
        "stop": "pkill -9 -f 'node server/api.js' || true"
    },
    {
        "id": "fiscalflow",
        "name": "FiscalFlow Wealth Platform",
        "desc": "FastAPI financial intelligence, ledger & analytics",
        "port": 8081,
        "vip": "192.168.0.184",
        "url": "http://192.168.0.182:8081/docs",
        "vip_url": "http://192.168.0.184/",
        "pattern": "FiscalFlow",
        "start": "nohup /home/server/apps/FiscalFlow/backend/.venv/bin/python3 -m uvicorn app.main:app --app-dir /home/server/apps/FiscalFlow/backend --host 0.0.0.0 --port 8081 >/home/server/fiscal.log 2>&1 &",
        "stop": "pkill -9 -f 'FiscalFlow' || true"
    },
    {
        "id": "madenmore-studio",
        "name": "MadeNMore 3D Creative Studio",
        "desc": "Next.js 16 (Turbopack) & React 19 App (Alps, CRM, ERP)",
        "port": 5175,
        "vip": "192.168.0.185",
        "url": "http://192.168.0.182:5175",
        "vip_url": "http://192.168.0.185/",
        "pattern": "5175",
        "start": "cd /home/server/apps/Stitch3DStudio/stitch_madenmore_3d_creative_studio && nohup npx next start -p 5175 -H 0.0.0.0 >/home/server/stitch3d.log 2>&1 &",
        "stop": "pkill -9 -f 'next start -p 5175' || true; pkill -9 -f 'next-server' || true"
    },
    {
        "id": "nginx-vips",
        "name": "Nginx VIP Gateway",
        "desc": "Virtual IP aliases (192.168.0.182–187) & Port 80 Reverse Proxy",
        "port": 80,
        "vip": "192.168.0.182–187",
        "url": "http://192.168.0.182/",
        "vip_url": "http://192.168.0.182/",
        "pattern": "nginx",
        "start": "bash /home/server/setup_virtual_ips.sh; echo 1 | sudo -S systemctl restart nginx || true",
        "stop": "echo 1 | sudo -S systemctl stop nginx || true"
    }
]


class ServiceActionWorker(QThread):
    finished_signal = Signal(str, str)  # action, message

    def __init__(self, cmd, host="192.168.0.182", user="server", password="1"):
        super().__init__()
        self.cmd = cmd
        self.host = host
        self.user = user
        self.password = password

    def run(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, username=self.user, password=self.password, timeout=8)
            stdin, stdout, stderr = client.exec_command(self.cmd)
            out = stdout.read().decode('utf-8', 'ignore')
            err = stderr.read().decode('utf-8', 'ignore')
            client.close()
            msg = out.strip() if out.strip() else (err.strip() if err.strip() else "Operation completed successfully.")
            self.finished_signal.emit("success", msg)
        except Exception as e:
            self.finished_signal.emit("error", str(e))


class StatusCheckerWorker(QThread):
    status_signal = Signal(dict)

    def __init__(self, host="192.168.0.182", user="server", password="1"):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password

    def run(self):
        status_map = {}
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, username=self.user, password=self.password, timeout=6)
            stdin, stdout, stderr = client.exec_command("ss -tulpn | grep LISTEN")
            listen_output = stdout.read().decode('utf-8', 'ignore')
            client.close()

            for srv in SERVICES_INFO:
                port_str = f":{srv['port']} "
                port_str2 = f":{srv['port']}\n"
                is_on = (port_str in listen_output or port_str2 in listen_output)
                status_map[srv["id"]] = is_on
        except Exception:
            for srv in SERVICES_INFO:
                status_map[srv["id"]] = False
        
        self.status_signal.emit(status_map)


class ServerManagementPage(QWidget):
    """Server-Side Hosted Websites & Services ON/OFF Management Console."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = {}
        self.init_ui()
        self.refresh_status()

        # Polling timer for live status updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_status)
        self.timer.start(5000)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        # Header Bar
        header_frame = QFrame()
        header_frame.setObjectName("Card")
        hl = QHBoxLayout(header_frame)
        hl.setContentsMargins(18, 14, 18, 14)

        title_vbox = QVBoxLayout()
        title_lbl = QLabel("🌐 Hosted Websites & Multi-App Server Control")
        title_lbl.setObjectName("HeaderTitle")
        title_vbox.addWidget(title_lbl)

        sub_lbl = QLabel("Turn ON, Turn OFF, restart individual web apps, and manage Virtual IPs on 192.168.0.182")
        sub_lbl.setObjectName("MetricSubtext")
        title_vbox.addWidget(sub_lbl)
        hl.addLayout(title_vbox)

        hl.addStretch()

        btn_refresh = QPushButton("🔄 Refresh Status")
        btn_refresh.setObjectName("SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_status)
        hl.addWidget(btn_refresh)

        btn_restart_all = QPushButton("⚡ Restart All Services")
        btn_restart_all.setObjectName("PrimaryButton")
        btn_restart_all.clicked.connect(self.restart_all_services)
        hl.addWidget(btn_restart_all)

        main_layout.addWidget(header_frame)

        # Scrollable Grid of Services
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        grid_container = QWidget()
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(14)

        row, col = 0, 0
        for srv in SERVICES_INFO:
            card = self.create_service_card(srv)
            self.cards[srv["id"]] = card
            self.grid_layout.addWidget(card["frame"], row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        scroll.setWidget(grid_container)
        main_layout.addWidget(scroll)

        # Bottom Console Output Box
        self.console_box = QTextEdit()
        self.console_box.setObjectName("TerminalBox")
        self.console_box.setReadOnly(True)
        self.console_box.setMaximumHeight(90)
        self.console_box.setPlaceholderText("Console logs and action outputs will appear here...")
        main_layout.addWidget(self.console_box)

    def create_service_card(self, srv):
        frame = QFrame()
        frame.setObjectName("Card")
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(16, 14, 16, 14)
        fl.setSpacing(10)

        # Card Top
        top_h = QHBoxLayout()
        name_lbl = QLabel(srv["name"])
        name_lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        top_h.addWidget(name_lbl)

        status_lbl = QLabel("🟡 CHECKING...")
        status_lbl.setStyleSheet("font-weight: bold; font-size: 11px; padding: 3px 8px; border-radius: 6px; background: rgba(255,255,255,0.05);")
        top_h.addWidget(status_lbl, alignment=Qt.AlignRight)
        fl.addLayout(top_h)

        desc_lbl = QLabel(srv["desc"])
        desc_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        desc_lbl.setWordWrap(True)
        fl.addWidget(desc_lbl)

        # Endpoints Box
        ep_box = QFrame()
        ep_box.setStyleSheet("background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 6px 10px;")
        epl = QVBoxLayout(ep_box)
        epl.setContentsMargins(4, 4, 4, 4)
        epl.setSpacing(4)

        vip_text = QLabel(f"🌐 Virtual IP: {srv['vip']} (Port 80)")
        vip_text.setStyleSheet("font-family: monospace; font-size: 11px; color: #818cf8;")
        epl.addWidget(vip_text)

        port_text = QLabel(f"🔌 Direct Port URL: {srv['url']}")
        port_text.setStyleSheet("font-family: monospace; font-size: 11px; color: #cbd5e1;")
        epl.addWidget(port_text)

        fl.addWidget(ep_box)

        # Action Buttons
        btn_h = QHBoxLayout()
        btn_on = QPushButton("▶ Turn ON")
        btn_on.setStyleSheet("background: #059669; color: white; font-weight: bold; font-size: 11px; padding: 6px 12px; border-radius: 6px;")
        btn_on.clicked.connect(lambda _, s=srv: self.start_service(s))
        btn_h.addWidget(btn_on)

        btn_off = QPushButton("⏹ Turn OFF")
        btn_off.setStyleSheet("background: #dc2626; color: white; font-weight: bold; font-size: 11px; padding: 6px 12px; border-radius: 6px;")
        btn_off.clicked.connect(lambda _, s=srv: self.stop_service(s))
        btn_h.addWidget(btn_off)

        btn_restart = QPushButton("🔄 Restart")
        btn_restart.setStyleSheet("background: #334155; color: white; font-size: 11px; padding: 6px 10px; border-radius: 6px;")
        btn_restart.clicked.connect(lambda _, s=srv: self.restart_service(s))
        btn_h.addWidget(btn_restart)

        btn_open = QPushButton("🌐 Open")
        btn_open.setStyleSheet("background: #4f46e5; color: white; font-weight: bold; font-size: 11px; padding: 6px 10px; border-radius: 6px;")
        btn_open.clicked.connect(lambda _, s=srv: webbrowser.open(s["vip_url"] or s["url"]))
        btn_h.addWidget(btn_open)

        fl.addLayout(btn_h)

        return {
            "frame": frame,
            "status_lbl": status_lbl,
            "btn_on": btn_on,
            "btn_off": btn_off,
            "btn_restart": btn_restart,
            "btn_open": btn_open
        }

    def refresh_status(self):
        self.checker = StatusCheckerWorker()
        self.checker.status_signal.connect(self.on_status_updated)
        self.checker.start()

    def on_status_updated(self, status_map):
        for srv_id, is_on in status_map.items():
            if srv_id in self.cards:
                card = self.cards[srv_id]
                if is_on:
                    card["status_lbl"].setText("🟢 ONLINE")
                    card["status_lbl"].setStyleSheet("font-weight: bold; font-size: 11px; padding: 3px 8px; border-radius: 6px; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3);")
                    card["btn_on"].setEnabled(False)
                    card["btn_off"].setEnabled(True)
                else:
                    card["status_lbl"].setText("🔴 STOPPED")
                    card["status_lbl"].setStyleSheet("font-weight: bold; font-size: 11px; padding: 3px 8px; border-radius: 6px; background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3);")
                    card["btn_on"].setEnabled(True)
                    card["btn_off"].setEnabled(False)

    def start_service(self, srv):
        self.console_box.append(f"[*] Starting service: {srv['name']}...")
        self.worker = ServiceActionWorker(srv["start"])
        self.worker.finished_signal.connect(lambda res, msg: (self.console_box.append(f"[OK] {srv['name']} started: {msg}"), self.refresh_status()))
        self.worker.start()

    def stop_service(self, srv):
        self.console_box.append(f"[*] Stopping service: {srv['name']}...")
        self.worker = ServiceActionWorker(srv["stop"])
        self.worker.finished_signal.connect(lambda res, msg: (self.console_box.append(f"[OK] {srv['name']} stopped: {msg}"), self.refresh_status()))
        self.worker.start()

    def restart_service(self, srv):
        self.console_box.append(f"[*] Restarting service: {srv['name']}...")
        cmd = f"{srv['stop']}; sleep 1; {srv['start']}"
        self.worker = ServiceActionWorker(cmd)
        self.worker.finished_signal.connect(lambda res, msg: (self.console_box.append(f"[OK] {srv['name']} restarted: {msg}"), self.refresh_status()))
        self.worker.start()

    def restart_all_services(self):
        self.console_box.append("[*] Restarting all hosted web services and Virtual IPs...")
        self.worker = ServiceActionWorker("bash /home/server/start_web_services.sh")
        self.worker.finished_signal.connect(lambda res, msg: (self.console_box.append(f"[OK] All services restarted: {msg}"), self.refresh_status()))
        self.worker.start()
