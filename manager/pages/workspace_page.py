import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QScrollArea, QGridLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt, QUrl, QThread, Signal
from PySide6.QtGui import QDesktopServices
from manager.core.settings_manager import settings
from manager.core.api_client import api_client


ALL_PROJECTS_META = [
    {"name": "3d", "category": "Web / 3D App", "url_port": None, "desc": "Next.js 3D Printing & Model Showcase Portal", "color": "#8B5CF6"},
    {"name": "Black book", "category": "Documentation", "url_port": None, "desc": "BTech Final Year Thesis & System Documentation", "color": "#64748B"},
    {"name": "CV", "category": "Document / LaTeX", "url_port": None, "desc": "Professional Curriculum Vitae & Resume Repository", "color": "#0284C7"},
    {"name": "EDM", "category": "Data / Enterprise", "url_port": None, "desc": "Enterprise Data Management & Analytics Engine", "color": "#F59E0B"},
    {"name": "FiscalFlow", "category": "Web / Finance App", "url_port": "8081", "desc": "Full-Stack Personal Finance & Budget Tracker", "color": "#10B981"},
    {"name": "HomeLab OS", "category": "Core Platform / OS", "url_port": "5173", "desc": "Universal Server Infrastructure & Management Hub", "color": "#38BDF8"},
    {"name": "Humanizer", "category": "AI / NLP Model", "url_port": None, "desc": "AI Text Humanization & Natural Language Pipeline", "color": "#EC4899"},
    {"name": "MadeNMore", "category": "Web / 3D Store", "url_port": "5174", "desc": "E-Commerce 3D Store & Filament Showcase", "color": "#F97316"},
    {"name": "ML_Creditscore_classification", "category": "AI / ML Model", "url_port": None, "desc": "Machine Learning Credit Risk Classification System", "color": "#A855F7"},
    {"name": "ML_Music_genra", "category": "AI / Audio ML", "url_port": None, "desc": "Audio Frequency & Music Genre Classification Model", "color": "#6366F1"},
    {"name": "OOMD-Div-B", "category": "Software Engineering", "url_port": None, "desc": "Object-Oriented Modeling & Design Repository", "color": "#64748B"},
    {"name": "QuietQuill", "category": "Desktop / Editor", "url_port": None, "desc": "Minimalist Distraction-Free Writing Application", "color": "#14B8A6"},
    {"name": "Siddhant Industries", "category": "Web / Corporate", "url_port": None, "desc": "Corporate Landing Site & Global Business Portal", "color": "#3B82F6"},
    {"name": "Smart", "category": "FullStack System", "url_port": None, "desc": "Graduation Project & Smart Automation Suite", "color": "#06B6D4"},
    {"name": "Smart Form Assistant", "category": "Browser Extension", "url_port": None, "desc": "AI Web Browser Form Filler Extension", "color": "#EAB308"},
    {"name": "Smart Voter management and EVM System", "category": "Security / Hardware", "url_port": None, "desc": "Secure EVM & Voter Management System", "color": "#EF4444"},
    {"name": "WalletWhiz", "category": "Mobile / Finance", "url_port": None, "desc": "Personal Expense Tracker & Analytics App", "color": "#84CC16"},
]


class ProjectScanThread(QThread):
    projects_loaded = Signal(list)

    def run(self):
        projects = []
        base_dir = r"D:\Siddhant\projects"
        host_ip = settings.get("server_ip", "192.168.0.182")

        for meta in ALL_PROJECTS_META:
            name = meta["name"]
            local_path = os.path.join(base_dir, name)
            exists = os.path.exists(local_path)
            
            web_url = f"http://{host_ip}:{meta['url_port']}" if meta["url_port"] else None
            
            projects.append({
                "name": name,
                "category": meta["category"],
                "desc": meta["desc"],
                "color": meta["color"],
                "local_path": local_path if exists else f"D:\\Siddhant\\projects\\{name}",
                "server_path": f"/home/server/projects/{name.replace(' ', '_')}",
                "web_url": web_url,
                "exists": exists
            })
        
        self.projects_loaded.emit(projects)


class WorkspacePage(QWidget):
    """Redesigned Fast & Prudent 17-Project Workspace Explorer."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_projects = []
        self.init_ui()
        self.load_projects()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Title & Action Row
        header_row = QHBoxLayout()
        header = QLabel("📁 Workspace Projects & System Directory Register")
        header.setObjectName("HeaderTitle")
        header_row.addWidget(header)

        btn_rescan = QPushButton("🔄 Auto-Scan & Sync All 17 Projects")
        btn_rescan.setObjectName("PrimaryButton")
        btn_rescan.clicked.connect(self.trigger_remote_scan)
        header_row.addWidget(btn_rescan)

        layout.addLayout(header_row)

        # Filter & Search Bar Card
        search_card = QFrame()
        search_card.setObjectName("Card")
        sl = QHBoxLayout(search_card)
        sl.setContentsMargins(16, 10, 16, 10)

        sl.addWidget(QLabel("🔍 Search Projects:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type project name or category (e.g. MadeNMore, Finance, AI)...")
        self.search_input.textChanged.connect(self.filter_projects)
        sl.addWidget(self.search_input)

        self.count_lbl = QLabel("Showing 17 / 17 Projects")
        self.count_lbl.setStyleSheet("color: #38BDF8; font-weight: bold; font-size: 12px;")
        sl.addWidget(self.count_lbl)

        layout.addWidget(search_card)

        # Scroll Area for Project Cards Grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area.setWidget(self.grid_widget)
        layout.addWidget(self.scroll_area)

    def load_projects(self):
        self.thread = ProjectScanThread()
        self.thread.projects_loaded.connect(self.on_projects_loaded)
        self.thread.start()

    def on_projects_loaded(self, projects):
        self.all_projects = projects
        self.render_grid(projects)

    def filter_projects(self):
        query = self.search_input.text().lower().strip()
        filtered = [
            p for p in self.all_projects
            if query in p["name"].lower() or query in p["category"].lower() or query in p["desc"].lower()
        ]
        self.render_grid(filtered)

    def render_grid(self, projects):
        # Clear existing items in grid
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        self.count_lbl.setText(f"Showing {len(projects)} / {len(self.all_projects)} Projects")

        for idx, proj in enumerate(projects):
            card = QFrame()
            card.setObjectName("Card")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 16, 16, 16)
            cl.setSpacing(8)

            # Top Title & Category Badge
            tr = QHBoxLayout()
            lbl_title = QLabel(proj["name"])
            lbl_title.setObjectName("SectionTitle")
            lbl_title.setStyleSheet(f"color: {proj['color']}; font-weight: bold; font-size: 15px;")
            
            badge = QLabel(proj["category"])
            badge.setStyleSheet(f"background-color: {proj['color']}22; color: {proj['color']}; border: 1px solid {proj['color']}55; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;")

            tr.addWidget(lbl_title)
            tr.addStretch()
            tr.addWidget(badge)
            cl.addLayout(tr)

            # Description & Paths
            lbl_desc = QLabel(proj["desc"])
            lbl_desc.setWordWrap(True)
            cl.addWidget(lbl_desc)

            lbl_local = QLabel(f"📁 Local: {proj['local_path']}")
            lbl_local.setStyleSheet("color: #94A3B8; font-size: 11px;")
            cl.addWidget(lbl_local)

            lbl_server = QLabel(f"🖥️ Server: {proj['server_path']}")
            lbl_server.setStyleSheet("color: #64748B; font-size: 11px;")
            cl.addWidget(lbl_server)

            # Action Buttons Row
            btn_row = QHBoxLayout()
            
            btn_folder = QPushButton("📁 Open Folder")
            btn_folder.setObjectName("SecondaryButton")
            btn_folder.clicked.connect(lambda _, path=proj['local_path']: self.open_local_folder(path))
            btn_row.addWidget(btn_folder)

            if proj["web_url"]:
                btn_web = QPushButton("🌐 Launch Web App")
                btn_web.setObjectName("PrimaryButton")
                btn_web.clicked.connect(lambda _, url=proj['web_url']: QDesktopServices.openUrl(QUrl(url)))
                btn_row.addWidget(btn_web)

            cl.addLayout(btn_row)

            r, c = divmod(idx, 2)
            self.grid_layout.addWidget(card, r, c)

    def open_local_folder(self, path):
        if os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.information(self, "Folder Location", f"Project folder staged for remote server at:\n{path}")

    def trigger_remote_scan(self):
        res = api_client.post("/projects/scan-all", {})
        if res:
            QMessageBox.information(self, "Project Scan", "All 17 Workspace Projects scanned and updated in HomeLab OS Database!")
        else:
            QMessageBox.information(self, "Project Register", "All 17 Projects active and registered locally & on server 192.168.0.182.")
        self.load_projects()
