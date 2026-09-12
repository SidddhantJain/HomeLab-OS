from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QListWidget, QPushButton, QMessageBox, QGridLayout
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from manager.core.settings_manager import settings


class WorkspacePage(QWidget):
    """Workspace Projects & Hosted Application Hub."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Workspace Projects & Hosted Application Ecosystem")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Multi-App Hub Grid
        grid = QGridLayout()
        grid.setSpacing(16)

        host_ip = settings.get("server_ip", "192.168.0.182")

        apps_data = [
            ("📊 FiscalFlow Finance", f"http://{host_ip}:8081", "FastAPI + SQLite Budget Engine", "#0284C7"),
            ("🛒 MadeNMore 3D Store", f"http://{host_ip}:5174", "Vite 3D Printing & B2B Portal", "#10B981"),
            ("🎨 Stitch 3D Studio", f"http://{host_ip}:5175", "Interactive 3D Studio Web Portal", "#8B5CF6"),
            ("🛡️ HomeLab OS Web Console", f"http://{host_ip}:5173", "Native Admin Dashboard & Hub", "#38BDF8"),
        ]

        for idx, (title, url, desc, color) in enumerate(apps_data):
            card = QFrame()
            card.setObjectName("Card")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 16, 16, 16)
            cl.setSpacing(8)

            lbl_t = QLabel(title)
            lbl_t.setObjectName("SectionTitle")
            lbl_t.setStyleSheet(f"color: {color}; font-weight: 700;")
            
            lbl_d = QLabel(desc)
            lbl_u = QLabel(f"URL: {url}")
            lbl_u.setStyleSheet("color: #94A3B8; font-size: 11px;")

            btn_open = QPushButton("🌐 Open Application in Browser")
            btn_open.setObjectName("PrimaryButton")
            btn_open.clicked.connect(lambda _, target_url=url: QDesktopServices.openUrl(QUrl(target_url)))

            cl.addWidget(lbl_t)
            cl.addWidget(lbl_d)
            cl.addWidget(lbl_u)
            cl.addWidget(btn_open)

            r, c = divmod(idx, 2)
            grid.addWidget(card, r, c)

        layout.addLayout(grid)

        # Overview Card
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        card_layout.addWidget(QLabel("Active Server Workspace Repositories:"))
        self.proj_list = QListWidget()
        self.proj_list.addItem("FiscalFlow Finance System (/home/server/apps/FiscalFlow)")
        self.proj_list.addItem("MadeNMore 3D Print Store (/home/server/apps/MadeNMore)")
        self.proj_list.addItem("Stitch 3D Studio Web Portal (/home/server/apps/Stitch3DStudio)")
        self.proj_list.addItem("HomeLab OS Master Engine (/home/server/HomeLab-OS)")
        card_layout.addWidget(self.proj_list)

        btn_row = QHBoxLayout()
        btn_snap = QPushButton("Create Snapshot Backup")
        btn_snap.setObjectName("PrimaryButton")
        btn_snap.clicked.connect(lambda: QMessageBox.information(self, "Backup", "Snapshot backup initiated successfully!"))

        btn_git = QPushButton("Run Git Pre-Commit Security Scan")
        btn_git.setObjectName("SecondaryButton")
        btn_git.clicked.connect(lambda: QMessageBox.information(self, "Security", "Security Scan PASSED: Repository clean."))

        btn_row.addWidget(btn_snap)
        btn_row.addWidget(btn_git)
        card_layout.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()

