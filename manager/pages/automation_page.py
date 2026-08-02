from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QMessageBox
from manager.widgets.workflow_builder import WorkflowBuilder


class AutomationPage(QWidget):
    """Visual Rule & Automation Workflow Builder Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Visual Rule Builder & Automation Engine")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Builder Canvas Container
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(10, 10, 10, 10)

        self.builder = WorkflowBuilder()
        self.builder.setMinimumHeight(400)
        cl.addWidget(self.builder)
        layout.addWidget(card)

        # Toolbar
        tb = QHBoxLayout()
        btn_add = QPushButton("Add New Rule Node")
        btn_add.setObjectName("PrimaryButton")
        btn_add.clicked.connect(lambda: QMessageBox.information(self, "Rule Builder", "Node added to canvas!"))

        btn_save = QPushButton("Save & Deploy Automation")
        btn_save.setObjectName("SecondaryButton")
        btn_save.clicked.connect(lambda: QMessageBox.information(self, "Rule Builder", "Automation workflow deployed to server!"))

        tb.addWidget(btn_add)
        tb.addWidget(btn_save)
        tb.addStretch()
        layout.addLayout(tb)
