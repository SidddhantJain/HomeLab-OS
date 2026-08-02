from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QCheckBox, QMessageBox
)
from manager.core.settings_manager import settings
import subprocess


class SettingsPage(QWidget):
    """Application & Server Connection Settings Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Manager Preferences & Server Profile Settings")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(14)

        cl.addWidget(QLabel("Target HomeLab Server Hostname / IP:"))
        self.ip_input = QLineEdit(settings.get("server_ip", "192.168.0.180"))
        cl.addWidget(self.ip_input)

        cl.addWidget(QLabel("FastAPI REST Port:"))
        self.port_input = QLineEdit(str(settings.get("server_port", 8000)))
        cl.addWidget(self.port_input)

        cl.addWidget(QLabel("RDP Protocol Port (Remote Desktop):"))
        self.rdp_port_input = QLineEdit(str(settings.get("rdp_port", 3389)))
        cl.addWidget(self.rdp_port_input)

        self.auto_conn = QCheckBox("Auto-connect to 192.168.0.180 on PySide6 application launch")
        self.auto_conn.setChecked(settings.get("auto_connect", True))
        cl.addWidget(self.auto_conn)

        btn_row = QHBoxLayout()
        btn_save = QPushButton("Save Settings Profile")
        btn_save.setObjectName("PrimaryButton")
        btn_save.clicked.connect(self.save_settings)

        btn_rdp = QPushButton("Launch Remote Desktop (mstsc / RDP)")
        btn_rdp.setObjectName("SecondaryButton")
        btn_rdp.clicked.connect(self.launch_rdp)

        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_rdp)
        cl.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()

    def save_settings(self):
        settings.set("server_ip", self.ip_input.text().strip())
        settings.set("server_port", int(self.port_input.text().strip()))
        settings.set("rdp_port", int(self.rdp_port_input.text().strip()))
        settings.set("auto_connect", self.auto_conn.isChecked())
        QMessageBox.information(self, "Settings", "Settings saved successfully!")

    def launch_rdp(self):
        target_ip = self.ip_input.text().strip()
        try:
            # On Windows, invoke mstsc /v:192.168.0.180
            subprocess.Popen(["mstsc", f"/v:{target_ip}"])
        except Exception as e:
            QMessageBox.warning(self, "RDP Launcher", f"Could not launch mstsc RDP client: {e}")
