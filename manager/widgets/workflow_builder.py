from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QPainter


class WorkflowBuilder(QGraphicsView):
    """Visual Automation Workflow Builder Graphics View (Trigger -> Condition -> Action)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor('#0F172A')))

        self.init_workflow()

    def init_workflow(self):
        self.scene.clear()

        # Workflow Nodes
        nodes = [
            {"title": "⚡ Trigger Node", "text": "Disk Storage > 90%", "x": 100, "y": 150, "color": "#F59E0B"},
            {"title": "🔍 Condition Node", "text": "Storage Pool = HDD /dev/sdb1", "x": 350, "y": 150, "color": "#0284C7"},
            {"title": "🚀 Action Node", "text": "Create Backup & Notify User", "x": 600, "y": 150, "color": "#10B981"}
        ]

        # Connect Nodes with arrows
        pen = QPen(QColor('#38BDF8'), 3)
        self.scene.addLine(280, 185, 350, 185, pen)
        self.scene.addLine(530, 185, 600, 185, pen)

        for n in nodes:
            rect = self.scene.addRect(n["x"], n["y"], 180, 70, QPen(QColor(n["color"]), 2), QBrush(QColor('#1E293B')))
            
            t_item = self.scene.addText(n["title"])
            t_item.setDefaultTextColor(QColor(n["color"]))
            t_item.setFont(QFont('Segoe UI', 9, QFont.Bold))
            t_item.setPos(n["x"] + 10, n["y"] + 8)

            d_item = self.scene.addText(n["text"])
            d_item.setDefaultTextColor(QColor('#CBD5E1'))
            d_item.setFont(QFont('Segoe UI', 8))
            d_item.setPos(n["x"] + 10, n["y"] + 32)
