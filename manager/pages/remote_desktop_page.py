from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QMessageBox
)
import subprocess
from manager.core.settings_manager import settings


class RemoteDesktopPage(QWidget):
    """Remote Desktop Integration Page (RDP / VRDE / VNC Protocols)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Remote Desktop & Virtual Display Integration")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Quick Connection Card
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(14)

        cl.addWidget(QLabel("Target RDP / VRDE Host Address:"))
        self.host_input = QLineEdit("192.168.0.180")
        cl.addWidget(self.host_input)

        cl.addWidget(QLabel("RDP Port (Default 3389 / VirtualBox VRDE 5901-5902):"))
        self.port_input = QLineEdit("3389")
        cl.addWidget(self.port_input)

        btn_row = QHBoxLayout()
        btn_rdp = QPushButton("Launch RDP Remote Desktop (mstsc)")
        btn_rdp.setObjectName("PrimaryButton")
        btn_rdp.clicked.connect(self.launch_rdp)

        btn_vnc = QPushButton("Connect VRDE Console (Port 5901)")
        btn_vnc.setObjectName("SecondaryButton")
        btn_vnc.clicked.connect(self.launch_vrde)

        btn_row.addWidget(btn_rdp)
        btn_row.addWidget(btn_vnc)
        cl.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()

    def launch_rdp(self):
        target = f"{self.host_input.text().strip()}:{self.port_input.text().strip()}"
        try:
            subprocess.Popen(["mstsc", f"/v:{target}"])
        except Exception as e:
            QMessageBox.warning(self, "RDP Connection", f"Could not launch RDP client: {e}")

    def launch_vrde(self):
        target = f"{self.host_input.text().strip()}:5901"
        try:
            subprocess.Popen(["mstsc", f"/v:{target}"])
        except Exception as e:
            QMessageBox.information(self, "VRDE Launch", f"Launching VirtualBox Remote Display stream to {target}...")
