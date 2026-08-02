from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFrame
)
from PySide6.QtCore import Qt
from manager.core.settings_manager import settings


class ServerLauncherDialog(QDialog):
    """Server Connection & Credentials Login Dialog for HomeLab Manager v1.5."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("HomeLab Manager v1.5 — Server Connection")
        self.resize(420, 360)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Connect to HomeLab Server")
        title.setObjectName("HeaderTitle")
        layout.addWidget(title)

        subtitle = QLabel("Enter server IP or select saved host profile:")
        subtitle.setObjectName("MetricSubtext")
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 16, 16, 16)
        cl.setSpacing(10)

        cl.addWidget(QLabel("Server Address / IP:"))
        self.ip_input = QLineEdit(settings.get("server_ip", "192.168.0.180"))
        cl.addWidget(self.ip_input)

        cl.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit(settings.get("username", "media-server"))
        cl.addWidget(self.user_input)

        cl.addWidget(QLabel("Password / SSH Key:"))
        self.pass_input = QLineEdit("1")
        self.pass_input.setEchoMode(QLineEdit.Password)
        cl.addWidget(self.pass_input)

        self.remember_cb = QCheckBox("Remember Server Credentials")
        self.remember_cb.setChecked(settings.get("remember_profile", True))
        cl.addWidget(self.remember_cb)

        layout.addWidget(card)

        btn_row = QHBoxLayout()
        btn_connect = QPushButton("Connect to Server ➔")
        btn_connect.setObjectName("PrimaryButton")
        btn_connect.clicked.connect(self.accept)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("SecondaryButton")
        btn_cancel.clicked.connect(self.reject)

        btn_row.addWidget(btn_connect)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)
