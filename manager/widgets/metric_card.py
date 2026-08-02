from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class MetricCard(QFrame):
    """Reusable metric KPI card with vibrant title, big value display, and trend badge."""
    def __init__(self, title: str, value: str, subtext: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("SectionTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("MetricValue")

        self.subtext_label = QLabel(subtext)
        self.subtext_label.setObjectName("MetricSubtext")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtext_label)

    def set_value(self, value: str, subtext: str = None):
        self.value_label.setText(value)
        if subtext is not None:
            self.subtext_label.setText(subtext)
