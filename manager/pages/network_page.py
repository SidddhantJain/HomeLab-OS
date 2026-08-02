from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from manager.widgets.topology_canvas import TopologyCanvas
from manager.core.api_client import api_client


class NetworkPage(QWidget):
    """Network Topology Map & Device Discovery Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Interactive Network Topology & Infrastructure Map")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Graphical Canvas Card
        canvas_card = QFrame()
        canvas_card.setObjectName("Card")
        cc_layout = QVBoxLayout(canvas_card)
        cc_layout.setContentsMargins(10, 10, 10, 10)

        self.canvas = TopologyCanvas()
        self.canvas.setMinimumHeight(450)
        cc_layout.addWidget(self.canvas)
        layout.addWidget(canvas_card)

        # Discovered Network Interfaces Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Device Hostname", "IP Address", "MAC Address", "Network Interface", "Status / Latency"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_devices()

    def populate_devices(self):
        devices = [
            {"host": "media-server", "ip": "192.168.0.180", "mac": "98:de:d0:16:af:8f", "iface": "wlx98ded016af8f", "status": "ONLINE (0.4 ms) 🟢"},
            {"host": "Gateway-Router", "ip": "192.168.0.1", "mac": "00:11:22:33:44:55", "iface": "br0", "status": "ONLINE (1.2 ms) 🟢"},
            {"host": "Docker-Bridge", "ip": "172.18.0.1", "mac": "02:42:56:73:db:0e", "iface": "br-906d518598dc", "status": "ACTIVE 🟢"}
        ]

        self.table.setRowCount(len(devices))
        for r, d in enumerate(devices):
            self.table.setItem(r, 0, QTableWidgetItem(d["host"]))
            self.table.setItem(r, 1, QTableWidgetItem(d["ip"]))
            self.table.setItem(r, 2, QTableWidgetItem(d["mac"]))
            self.table.setItem(r, 3, QTableWidgetItem(d["iface"]))
            self.table.setItem(r, 4, QTableWidgetItem(d["status"]))
