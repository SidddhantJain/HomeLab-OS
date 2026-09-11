from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
import requests
from manager.core.settings_manager import settings


class MobileSyncPage(QWidget):
    """PySide6 Manager Page for Android Companion, WebRTC Terminal & Media Deduplication."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Android Native Companion & WebRTC Remote Terminal")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Overview Card
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.addWidget(QLabel("Mobile Sync Engine Features:"))
        cl.addWidget(QLabel(" • FCM Push Alerts & Biometric Authentication"))
        cl.addWidget(QLabel(" • Low-Latency P2P WebRTC Remote Terminal Streaming"))
        cl.addWidget(QLabel(" • Client-Side SHA-256 Media Auto-Upload Deduplication"))
        layout.addWidget(card)

        # Devices Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Device ID", "Device Name", "Platform", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_devices()

    def populate_devices(self):
        devs = [
            {"id": "dev-pixel7-01", "name": "Google Pixel 7 Pro", "platform": "Android 14", "status": "ONLINE 🟢"},
            {"id": "dev-galaxy-s23", "name": "Samsung Galaxy S23 Ultra", "platform": "Android 14", "status": "PAIRED 🟡"}
        ]
        self.table.setRowCount(len(devs))
        for r, item in enumerate(devs):
            self.table.setItem(r, 0, QTableWidgetItem(item["id"]))
            self.table.setItem(r, 1, QTableWidgetItem(item["name"]))
            self.table.setItem(r, 2, QTableWidgetItem(item["platform"]))
            self.table.setItem(r, 3, QTableWidgetItem(item["status"]))
