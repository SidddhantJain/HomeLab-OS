from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QProgressBar
)
from manager.core.api_client import api_client


class StoragePage(QWidget):
    """Storage & SMART Drive Health Manager Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Storage Pools & SMART Drive Diagnostics")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Drive Inventory Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Device Node", "Drive Model", "Capacity", "Mount Path", "SMART Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Populate static/polled storage data
        self.populate_storage_table()

    def populate_storage_table(self):
        drives = [
            {
                "dev": "/dev/sda2",
                "model": "ADATA SP550 SSD",
                "capacity": "240 GB",
                "mount": "/",
                "smart": "HEALTHY (PASSED 🟢)",
                "action": "Unmount Disabled"
            },
            {
                "dev": "/dev/sdb1",
                "model": "Super Top M6116 External HDD",
                "capacity": "1,000 GB (932 GiB)",
                "mount": "/media/media-server/6E18C6FD18C6C377",
                "smart": "HEALTHY (PASSED 🟢)",
                "action": "Safe Unmount"
            }
        ]

        self.table.setRowCount(len(drives))
        for row, drive in enumerate(drives):
            self.table.setItem(row, 0, QTableWidgetItem(drive["dev"]))
            self.table.setItem(row, 1, QTableWidgetItem(drive["model"]))
            self.table.setItem(row, 2, QTableWidgetItem(drive["capacity"]))
            self.table.setItem(row, 3, QTableWidgetItem(drive["mount"]))
            self.table.setItem(row, 4, QTableWidgetItem(drive["smart"]))
            
            btn = QPushButton(drive["action"])
            btn.setObjectName("SecondaryButton")
            self.table.setCellWidget(row, 5, btn)
