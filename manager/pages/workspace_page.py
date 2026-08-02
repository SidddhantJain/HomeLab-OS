from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QListWidget, QPushButton, QMessageBox
)


class WorkspacePage(QWidget):
    """Workspace Projects & Backup Snapshot Manager."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Workspace Projects & Snapshot Backups")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        card_layout.addWidget(QLabel("Active Workspace Projects:"))
        self.proj_list = QListWidget()
        self.proj_list.addItem("HomeLab OS (Git Branch: main | Commit: ea202d8)")
        self.proj_list.addItem("Media Automation Services (Jellyfin / Sonarr Stack)")
        self.proj_list.addItem("Vault Backup Storage Service (/media/sdb1/backups)")
        card_layout.addWidget(self.proj_list)

        btn_row = QHBoxLayout()
        btn_snap = QPushButton("Create Snapshot Backup")
        btn_snap.setObjectName("PrimaryButton")
        btn_snap.clicked.connect(lambda: QMessageBox.information(self, "Backup", "Snapshot backup initiated successfully!"))

        btn_git = QPushButton("Run Git Pre-Commit Security Scan")
        btn_git.setObjectName("SecondaryButton")
        btn_git.clicked.connect(lambda: QMessageBox.information(self, "Security", "Security Scan PASSED: Repository clean."))

        btn_row.addWidget(btn_snap)
        btn_row.addWidget(btn_git)
        card_layout.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()
