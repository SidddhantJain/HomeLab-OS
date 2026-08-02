from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton, QMessageBox
)


class PluginsPage(QWidget):
    """Plugin Ecosystem App Center."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Plugin Ecosystem & One-Click App Store")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        grid = QGridLayout()
        grid.setSpacing(16)

        apps = [
            {"name": "Jellyfin Media Server", "desc": "Free software media system", "status": "Installed 🟢"},
            {"name": "Nextcloud Hub", "desc": "Self-hosted cloud storage", "status": "Available"},
            {"name": "Gitea Git Server", "desc": "Painless self-hosted Git service", "status": "Installed 🟢"},
            {"name": "Immich Photo Backup", "desc": "High performance photo & video backup", "status": "Available"},
            {"name": "Grafana Dashboards", "desc": "Operational intelligence & metrics", "status": "Available"},
            {"name": "Pi-hole DNS Sinkhole", "desc": "Network-wide ad blocking", "status": "Available"},
            {"name": "Vaultwarden Password Manager", "desc": "Lightweight Bitwarden server", "status": "Available"}
        ]

        for idx, app in enumerate(apps):
            r, c = idx // 2, idx % 2
            card = QFrame()
            card.setObjectName("Card")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 16, 16, 16)

            t_lbl = QLabel(app["name"])
            t_lbl.setObjectName("SectionTitle")
            d_lbl = QLabel(app["desc"])
            d_lbl.setObjectName("MetricSubtext")
            s_lbl = QLabel(f"Status: {app['status']}")

            btn = QPushButton("Install App" if "Available" in app["status"] else "Manage App")
            btn.setObjectName("PrimaryButton" if "Available" in app["status"] else "SecondaryButton")
            btn.clicked.connect(lambda _, a=app["name"]: QMessageBox.information(self, "App Store", f"Processing action for {a}..."))

            cl.addWidget(t_lbl)
            cl.addWidget(d_lbl)
            cl.addWidget(s_lbl)
            cl.addWidget(btn)

            grid.addWidget(card, r, c)

        layout.addLayout(grid)
        layout.addStretch()
