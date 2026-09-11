from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from manager.core.settings_manager import settings


class WasmPluginsPage(QWidget):
    """PySide6 Manager Page for WASM / WASI Plugin Sandbox."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("WASM / WASI Plugin Sandbox (Wasmtime Runtime)")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Plugin ID", "Name", "Language", "Sandbox Isolation", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_plugins()

    def populate_plugins(self):
        plugins = [
            {"id": "wasm-media-indexer", "name": "WASM High-Speed Media Indexer", "lang": "Rust (wasm32-wasi)", "isolation": "STRICT_WASI", "status": "LOADED 🟢"},
            {"id": "wasm-crypto-hasher", "name": "WASM BLAKE3 Hash Generator", "lang": "Go (wasm32-wasi)", "isolation": "STRICT_WASI", "status": "IDLE 🟡"}
        ]
        self.table.setRowCount(len(plugins))
        for r, item in enumerate(plugins):
            self.table.setItem(r, 0, QTableWidgetItem(item["id"]))
            self.table.setItem(r, 1, QTableWidgetItem(item["name"]))
            self.table.setItem(r, 2, QTableWidgetItem(item["lang"]))
            self.table.setItem(r, 3, QTableWidgetItem(item["isolation"]))
            self.table.setItem(r, 4, QTableWidgetItem(item["status"]))
