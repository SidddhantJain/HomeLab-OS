from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from manager.core.api_client import api_client


class DockerPage(QWidget):
    """Docker Container Engine & Stack Deployment Manager."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Docker Container Orchestration Engine")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Container Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Container ID / Name", "Image", "Status", "Ports", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_containers()

    def populate_containers(self):
        containers = [
            {"name": "homelab-backend", "image": "python:3.12-slim", "status": "running 🟢", "ports": "8000:8000"},
            {"name": "homelab-frontend", "image": "node:18-alpine", "status": "running 🟢", "ports": "5173:5173"},
            {"name": "postgres-db", "image": "postgres:16-alpine", "status": "stopped 🔴", "ports": "5432:5432"},
            {"name": "redis-cache", "image": "redis:7-alpine", "status": "running 🟢", "ports": "6379:6379"}
        ]

        self.table.setRowCount(len(containers))
        for r, c in enumerate(containers):
            self.table.setItem(r, 0, QTableWidgetItem(c["name"]))
            self.table.setItem(r, 1, QTableWidgetItem(c["image"]))
            self.table.setItem(r, 2, QTableWidgetItem(c["status"]))
            self.table.setItem(r, 3, QTableWidgetItem(c["ports"]))

            btn_box = QHBoxLayout()
            btn_restart = QPushButton("Restart")
            btn_restart.setObjectName("SecondaryButton")
            self.table.setCellWidget(r, 4, btn_restart)
