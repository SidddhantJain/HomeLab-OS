from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QStackedWidget, QLabel, QStatusBar, QDockWidget
)
from PySide6.QtCore import Qt

from manager.pages.dashboard_page import DashboardPage
from manager.pages.monitoring_page import MonitoringPage
from manager.pages.storage_page import StoragePage
from manager.pages.vault_page import VaultPage
from manager.pages.docker_page import DockerPage
from manager.pages.workspace_page import WorkspacePage
from manager.pages.plugins_page import PluginsPage
from manager.pages.network_page import NetworkPage
from manager.pages.console_page import ConsolePage
from manager.pages.automation_page import AutomationPage
from manager.pages.settings_page import SettingsPage


class HomeLabMainWindow(QMainWindow):
    """Main Application Window for HomeLab OS v1.5 Native Desktop Console."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HomeLab OS v1.5 — Desktop Manager Console")
        self.resize(1300, 850)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar Navigation Frame
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(16, 20, 16, 20)
        s_layout.setSpacing(8)

        logo_lbl = QLabel("🛡️ HomeLab OS v1.5")
        logo_lbl.setObjectName("HeaderTitle")
        s_layout.addWidget(logo_lbl)

        sub_lbl = QLabel("Native PySide6 Desktop Console")
        sub_lbl.setObjectName("MetricSubtext")
        s_layout.addWidget(sub_lbl)
        s_layout.addSpacing(16)

        # Navigation Stack
        self.pages_stack = QStackedWidget()

        # Nav Buttons Mapping
        self.nav_buttons = []
        nav_items = [
            ("📊 Dashboard", DashboardPage()),
            ("📈 Real-Time Monitoring", MonitoringPage()),
            ("💾 Storage & SMART", StoragePage()),
            ("🔒 LUKS Vault", VaultPage()),
            ("🐳 Docker Stack", DockerPage()),
            ("📁 Workspace", WorkspacePage()),
            ("🌐 Network Map", NetworkPage()),
            ("🖥️ Remote Console", ConsolePage()),
            ("⚡ Visual Automation", AutomationPage()),
            ("🔌 Plugin Store", PluginsPage()),
            ("⚙️ Settings", SettingsPage())
        ]

        for idx, (title, page) in enumerate(nav_items):
            self.pages_stack.addWidget(page)
            btn = QPushButton(title)
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, index=idx: self.switch_page(index))
            s_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        s_layout.addStretch()

        # Footer Server Profile Card
        footer_card = QFrame()
        footer_card.setObjectName("Card")
        fl = QVBoxLayout(footer_card)
        fl.setContentsMargins(10, 10, 10, 10)
        fl.addWidget(QLabel("Target Server:"))
        fl.addWidget(QLabel("media-server@192.168.0.180"))
        s_layout.addWidget(footer_card)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages_stack)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Connected to HomeLab Server: media-server@192.168.0.180 (Status: 200 OK)")

        # Activate initial Dashboard page
        self.switch_page(0)

    def switch_page(self, index: int):
        self.pages_stack.setCurrentIndex(index)
        for idx, btn in enumerate(self.nav_buttons):
            btn.setChecked(idx == index)
