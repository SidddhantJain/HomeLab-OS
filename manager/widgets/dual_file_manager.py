from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel, QFrame, QPushButton, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
import os


class DualFileManager(QWidget):
    """WinSCP / Total Commander style Dual-Pane File Explorer (Local PC <-> HomeLab Server)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Splitter Layout (Left Pane: Local PC | Right Pane: HomeLab Server)
        panes_layout = QHBoxLayout()

        # --- LEFT PANE: LOCAL PC ---
        left_frame = QFrame()
        left_frame.setObjectName("Card")
        l_layout = QVBoxLayout(left_frame)

        l_header = QLabel("🖥️ Local Host PC (Windows)")
        l_header.setObjectName("SectionTitle")
        l_layout.addWidget(l_header)

        self.local_tree = QTreeWidget()
        self.local_tree.setHeaderLabels(["Filename", "Size", "Type"])
        self.local_tree.header().setSectionResizeMode(QHeaderView.Stretch)
        l_layout.addWidget(self.local_tree)

        # --- RIGHT PANE: HOMELAB SERVER ---
        right_frame = QFrame()
        right_frame.setObjectName("Card")
        r_layout = QVBoxLayout(right_frame)

        r_header = QLabel("🐧 HomeLab Server (media-server@192.168.0.180)")
        r_header.setObjectName("SectionTitle")
        r_layout.addWidget(r_header)

        self.remote_tree = QTreeWidget()
        self.remote_tree.setHeaderLabels(["Filename", "Size", "Permissions"])
        self.remote_tree.header().setSectionResizeMode(QHeaderView.Stretch)
        r_layout.addWidget(self.remote_tree)

        panes_layout.addWidget(left_frame)
        panes_layout.addWidget(right_frame)
        layout.addLayout(panes_layout)

        # Action Button Toolbar (Upload, Download, Refresh, Delete)
        toolbar = QHBoxLayout()

        btn_upload = QPushButton("Upload Selection ➔")
        btn_upload.setObjectName("PrimaryButton")
        btn_upload.clicked.connect(lambda: QMessageBox.information(self, "Transfer", "Uploading file to media-server@192.168.0.180..."))

        btn_download = QPushButton("⬅ Download Selection")
        btn_download.setObjectName("SecondaryButton")
        btn_download.clicked.connect(lambda: QMessageBox.information(self, "Transfer", "Downloading file to local machine..."))

        btn_delete = QPushButton("Delete File 🗑️")
        btn_delete.setObjectName("DangerButton")

        toolbar.addWidget(btn_upload)
        toolbar.addWidget(btn_download)
        toolbar.addWidget(btn_delete)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        self.populate_trees()

    def populate_trees(self):
        # Local Files Mock Data
        local_files = [
            ("release_notes_v1.0.0.pdf", "1.2 MB", "Document"),
            ("homelab_backup_2026.tar.gz", "450 MB", "Archive"),
            ("docker-compose.yml", "4 KB", "YAML Config")
        ]
        for f, s, t in local_files:
            item = QTreeWidgetItem([f, s, t])
            self.local_tree.addTopLevelItem(item)

        # Remote Files Mock Data
        remote_files = [
            ("/home/media-server/HomeLab-OS", "Folder", "drwxr-xr-x"),
            ("/media/media-server/6E18C6FD18C6C377", "932 GB HDD", "drwxrwxrwx"),
            ("homelab_backend.log", "15 KB", "-rw-r--r--"),
            ("homelab.db", "28 KB", "-rw-r--r--")
        ]
        for f, s, p in remote_files:
            item = QTreeWidgetItem([f, s, p])
            self.remote_tree.addTopLevelItem(item)
