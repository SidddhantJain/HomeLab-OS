from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from manager.widgets.dual_file_manager import DualFileManager
from manager.widgets.remote_terminal import RemoteTerminalWidget


class ConsolePage(QWidget):
    """Remote Console, SSH Shell & Dual-Pane File Manager Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Remote Console & Dual-Pane File Transfer")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Tab Widget for Console Tools
        tabs = QTabWidget()
        tabs.addTab(RemoteTerminalWidget(), "🖥️ Tabbed SSH Terminal")
        tabs.addTab(DualFileManager(), "📁 Dual-Pane File Manager (WinSCP Style)")

        layout.addWidget(tabs)
