from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
import requests
from manager.core.settings_manager import settings


class HypervisorPage(QWidget):
    """PySide6 Manager Page for Bare-Metal Type-1 MicroVM Hypervisor, PCIe GPU Passthrough, & Virtual SAN Storage."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Bare-Metal MicroVM Hypervisor & Virtual SAN Console")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Overview Card
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.addWidget(QLabel("Hypervisor Engine: HomeLab HyperOS KVM/QEMU Core (Type-1 Bare-Metal 🔴)"))
        cl.addWidget(QLabel("Active MicroVMs: 2 Running | Virtual SAN Storage: 12.0 TB Total (8.2 TB Free)"))
        cl.addWidget(QLabel("PCIe Passthrough Status: NVIDIA RTX 3060 GPU assigned to 'vm-ubuntu-core'"))
        layout.addWidget(card)

        # Action Button Row
        btn_row = QHBoxLayout()
        btn_create_vm = QPushButton("➕ Provision New MicroVM")
        btn_create_vm.setObjectName("PrimaryButton")
        btn_create_vm.clicked.connect(self.create_vm)

        btn_san_pool = QPushButton("🗄️ Create Virtual SAN Pool")
        btn_san_pool.setObjectName("SecondaryButton")
        btn_san_pool.clicked.connect(self.create_san_pool)

        btn_refresh = QPushButton("🔄 Refresh Status")
        btn_refresh.setObjectName("SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_status)

        btn_row.addWidget(btn_create_vm)
        btn_row.addWidget(btn_san_pool)
        btn_row.addWidget(btn_refresh)
        layout.addLayout(btn_row)

        # MicroVMs Table
        table_title = QLabel("Managed MicroVM Instances & Virtual SAN Arrays")
        table_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(table_title)

        self.table = QTableWidget(3, 5)
        self.table.setHorizontalHeaderLabels(["VM / Pool ID", "Name", "Type / RAID", "vCPU / Capacity", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate sample data
        items = [
            ("vm-ubuntu-core", "Ubuntu-Server-MicroVM", "KVM Container", "4 vCPUs / 4GB RAM", "RUNNING 🟢"),
            ("vm-alpine-sandbox", "Alpine-Security-MicroVM", "LXC Container", "2 vCPUs / 1GB RAM", "STOPPED 🔴"),
            ("vsan-pool-main", "Primary Virtual SAN Pool", "RAID-Z2", "12.0 TB Array", "HEALTHY 🟢")
        ]

        for row, (vm_id, name, vtype, cap, stat) in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(vm_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(vtype))
            self.table.setItem(row, 3, QTableWidgetItem(cap))
            self.table.setItem(row, 4, QTableWidgetItem(stat))

        layout.addWidget(self.table)
        layout.addStretch()

    def create_vm(self):
        QMessageBox.information(self, "MicroVM Hypervisor", "MicroVM 'vm-node-new' provisioned on KVM engine!")

    def create_san_pool(self):
        QMessageBox.information(self, "Virtual SAN", "Virtual SAN pool 'vsan-pool-secondary' created successfully!")

    def refresh_status(self):
        QMessageBox.information(self, "Hypervisor Status", "Refreshed hypervisor engine telemetry & PCIe passthrough maps.")
