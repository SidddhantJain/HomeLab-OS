from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QProgressBar, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from manager.widgets.metric_card import MetricCard
from manager.core.api_client import api_client


class DashboardPage(QWidget):
    """Main System Dashboard page displaying live server telemetry, status badges, & health overview."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        # Timer for live telemetry polling (every 3 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_telemetry)
        self.timer.start(3000)
        self.refresh_telemetry()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header Title & Refresh Button
        header_layout = QHBoxLayout()
        title = QLabel("HomeLab OS Server Dashboard")
        title.setObjectName("HeaderTitle")
        
        self.refresh_btn = QPushButton("Refresh Telemetry")
        self.refresh_btn.setObjectName("SecondaryButton")
        self.refresh_btn.clicked.connect(self.refresh_telemetry)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        layout.addLayout(header_layout)

        # Metric KPI Cards Row
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)

        self.card_status = MetricCard("Server Status", "Connecting...", "Dell Inspiron 5558")
        self.card_cpu = MetricCard("CPU Utilization", "-- %", "Intel Core i7-5500U")
        self.card_ram = MetricCard("RAM Memory", "-- GB", "8GB SODIMM DDR3")
        self.card_temp = MetricCard("Core Thermals", "-- °C", "Dell SMM Sensor")

        grid_layout.addWidget(self.card_status, 0, 0)
        grid_layout.addWidget(self.card_cpu, 0, 1)
        grid_layout.addWidget(self.card_ram, 0, 2)
        grid_layout.addWidget(self.card_temp, 0, 3)
        layout.addLayout(grid_layout)

        # Main Overview Card: Server Details & Live Resource Bars
        overview_card = QFrame()
        overview_card.setObjectName("Card")
        ov_layout = QVBoxLayout(overview_card)
        ov_layout.setContentsMargins(20, 20, 20, 20)
        ov_layout.setSpacing(14)

        ov_title = QLabel("System Hardware & OS Diagnostics")
        ov_title.setObjectName("SectionTitle")
        ov_layout.addWidget(ov_title)

        self.lbl_server_name = QLabel("Server Host: media-server@192.168.0.180")
        self.lbl_os = QLabel("OS Release: Linux 6.8.0-51-generic (Ubuntu 24.04 LTS)")
        self.lbl_uptime = QLabel("Uptime: Active")

        ov_layout.addWidget(self.lbl_server_name)
        ov_layout.addWidget(self.lbl_os)
        ov_layout.addWidget(self.lbl_uptime)

        # CPU Usage Bar
        ov_layout.addWidget(QLabel("CPU Core Load:"))
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(0)
        self.cpu_bar.setStyleSheet("QProgressBar::chunk { background-color: #38BDF8; border-radius: 4px; }")
        ov_layout.addWidget(self.cpu_bar)

        # RAM Usage Bar
        ov_layout.addWidget(QLabel("RAM Memory Load:"))
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setValue(0)
        self.ram_bar.setStyleSheet("QProgressBar::chunk { background-color: #10B981; border-radius: 4px; }")
        ov_layout.addWidget(self.ram_bar)

        layout.addWidget(overview_card)
        layout.addStretch()

    def refresh_telemetry(self):
        data = api_client.get_system_status()
        if data:
            self.card_status.set_value("ACTIVE 🟢", data.get("server_name", "media-server"))
            cpu = data.get("cpu", 0.0)
            ram = data.get("ram", 0.0)
            temp = data.get("temperature", 40.0)
            mem_gb = data.get("memory_total_gb", 8.0)

            self.card_cpu.set_value(f"{cpu:.1f} %", "Dynamic Load")
            self.card_ram.set_value(f"{ram:.1f} %", f"Total: {mem_gb:.1f} GB")
            self.card_temp.set_value(f"{temp:.1f} °C", "Dell Fan: 2200 RPM")

            self.lbl_server_name.setText(f"Server Host: {data.get('server_name', 'media-server')}")
            self.lbl_os.setText(f"OS Release: {data.get('operating_system', 'Linux')}")
            self.lbl_uptime.setText(f"System Status: {data.get('uptime', 'Active')}")

            self.cpu_bar.setValue(int(cpu))
            self.ram_bar.setValue(int(ram))
        else:
            self.card_status.set_value("OFFLINE 🔴", "Check 192.168.0.180:8000")
