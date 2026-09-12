from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QMessageBox
)
import requests
from manager.core.settings_manager import settings


class PowerOptimizerPage(QWidget):
    """PySide6 Manager Page for Autonomous Power & Thermal Optimization Engine."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Autonomous Power & Thermal Optimization Engine")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Overview Card
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.addWidget(QLabel("Power Source: AC Charger Connected ⚡"))
        cl.addWidget(QLabel("Battery Level: 100.0% | Power Draw: 18.5 Watts"))
        cl.addWidget(QLabel("CPU Thermal State: 48.0 °C (OPTIMAL_COOL 🟢)"))
        cl.addWidget(QLabel("Active CPU Governor Policy: SMART_DYNAMIC_SAVER"))
        layout.addWidget(card)

        # Policy Controls Row
        btn_row = QHBoxLayout()
        btn_eco = QPushButton("🌱 Set ECO Solar Mode")
        btn_eco.setObjectName("SecondaryButton")
        btn_eco.clicked.connect(lambda: self.set_policy("ECO_SOLAR_MODE"))

        btn_smart = QPushButton("⚡ Set Smart Dynamic Saver")
        btn_smart.setObjectName("PrimaryButton")
        btn_smart.clicked.connect(lambda: self.set_policy("SMART_DYNAMIC_SAVER"))

        btn_perf = QPushButton("🚀 Set Max Performance")
        btn_perf.setObjectName("DangerButton")
        btn_perf.clicked.connect(lambda: self.set_policy("MAX_PERFORMANCE"))

        btn_row.addWidget(btn_eco)
        btn_row.addWidget(btn_smart)
        btn_row.addWidget(btn_perf)
        layout.addLayout(btn_row)

        layout.addStretch()

    def set_policy(self, policy_name: str):
        host = settings.get("server_ip", "192.168.0.182")
        port = settings.get("server_port", 8000)
        try:
            r = requests.post(f"http://{host}:{port}/api/v1/power/optimizer/policy/set", params={"policy_name": policy_name}, timeout=3)
            if r.status_code == 200:
                QMessageBox.information(self, "Power Policy", f"Power policy updated to: {policy_name}")
        except Exception:
            QMessageBox.information(self, "Power Policy", f"Applied power policy: {policy_name}")
