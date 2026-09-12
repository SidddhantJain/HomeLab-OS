from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from manager.core.settings_manager import settings


class NVRAnalyticsPage(QWidget):
    """PySide6 Manager Page for Frigate NVR Camera Video Analytics."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Smart Frigate NVR Video Analytics & AI Object Detection")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Event ID", "Camera Feed", "AI Label", "Confidence", "Detected Time"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_events()

    def populate_events(self):
        events = [
            {"id": "evt-ai-991", "camera": "Front Porch 4K", "label": "Person Detected 👤", "confidence": "96.0%", "time": "12 mins ago"},
            {"id": "evt-ai-988", "camera": "Driveway Wide", "label": "Vehicle Detected 🚗", "confidence": "92.0%", "time": "45 mins ago"}
        ]
        self.table.setRowCount(len(events))
        for r, item in enumerate(events):
            self.table.setItem(r, 0, QTableWidgetItem(item["id"]))
            self.table.setItem(r, 1, QTableWidgetItem(item["camera"]))
            self.table.setItem(r, 2, QTableWidgetItem(item["label"]))
            self.table.setItem(r, 3, QTableWidgetItem(item["confidence"]))
            self.table.setItem(r, 4, QTableWidgetItem(item["time"]))
