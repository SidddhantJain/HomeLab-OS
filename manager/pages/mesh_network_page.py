from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from manager.core.settings_manager import settings


class MeshNetworkPage(QWidget):
    """PySide6 Manager Page for Zero-Trust WireGuard & Tailscale Mesh Network."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Zero-Trust WireGuard & Tailscale Mesh Network Overlay")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Peer ID", "Device Name", "Mesh IP", "Protocol", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_peers()

    def populate_peers(self):
        peers = [
            {"id": "peer-laptop-01", "name": "Dell Inspiron 5558 (Primary Node)", "ip": "100.64.0.1", "proto": "WireGuard Mesh", "status": "CONNECTED 🟢"},
            {"id": "peer-pixel7-01", "name": "Google Pixel 7 Pro", "ip": "100.64.0.2", "proto": "Tailscale Mesh", "status": "ACTIVE 🟢"}
        ]
        self.table.setRowCount(len(peers))
        for r, item in enumerate(peers):
            self.table.setItem(r, 0, QTableWidgetItem(item["id"]))
            self.table.setItem(r, 1, QTableWidgetItem(item["name"]))
            self.table.setItem(r, 2, QTableWidgetItem(item["ip"]))
            self.table.setItem(r, 3, QTableWidgetItem(item["proto"]))
            self.table.setItem(r, 4, QTableWidgetItem(item["status"]))
