from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QPainter


class TopologyCanvas(QGraphicsView):
    """Interactive Graphical Network Topology Canvas using Qt QGraphicsView."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor('#0F172A')))

        self.init_topology()

    def init_topology(self):
        self.scene.clear()

        # Define Network Nodes
        nodes = [
            {"id": "cloud", "label": "🌐 Internet Cloud\n0.0.0.0/0", "x": 350, "y": 40, "color": "#0284C7", "active": True},
            {"id": "router", "label": "📡 Central Gateway Router\n192.168.0.1", "x": 350, "y": 140, "color": "#10B981", "active": True},
            {"id": "server", "label": "💻 HomeLab Server (Dell 5558)\n192.168.0.180 (Master Host)", "x": 350, "y": 270, "color": "#38BDF8", "active": True},
            {"id": "laptop", "label": "💻 Dev Laptop\n192.168.0.105", "x": 120, "y": 400, "color": "#94A3B8", "active": True},
            {"id": "nas", "label": "🗄️ External NAS / Vault\n/dev/sdb1 (932 GB)", "x": 280, "y": 400, "color": "#F59E0B", "active": True},
            {"id": "tv", "label": "📺 Living Room Smart TV\n192.168.0.120", "x": 440, "y": 400, "color": "#94A3B8", "active": True},
            {"id": "printer", "label": "🖨️ Network Printer\n192.168.0.150", "x": 600, "y": 400, "color": "#64748B", "active": True}
        ]

        # Draw Connections (Lines)
        lines = [
            ("cloud", "router"),
            ("router", "server"),
            ("server", "laptop"),
            ("server", "nas"),
            ("server", "tv"),
            ("server", "printer")
        ]

        node_map = {}
        for n in nodes:
            node_map[n["id"]] = n

        pen = QPen(QColor('#334155'), 3)
        for src_id, dst_id in lines:
            s, d = node_map[src_id], node_map[dst_id]
            self.scene.addLine(s["x"] + 60, s["y"] + 25, d["x"] + 60, d["y"] + 25, pen)

        # Draw Node Cards
        for n in nodes:
            rect = self.scene.addRect(n["x"], n["y"], 150, 50, QPen(QColor(n["color"]), 2), QBrush(QColor('#1E293B')))
            
            # Active LED Indicator
            led = self.scene.addEllipse(n["x"] + 125, n["y"] + 10, 10, 10, QPen(Qt.NoPen), QBrush(QColor('#10B981')))

            txt = self.scene.addText(n["label"])
            txt.setDefaultTextColor(QColor('#F8FAFC'))
            txt.setFont(QFont('Segoe UI', 8, QFont.Bold))
            txt.setPos(n["x"] + 8, n["y"] + 6)
