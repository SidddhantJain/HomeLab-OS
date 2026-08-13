"""
HomeLab OS Desktop Manager — System Tray Daemon & Background Status Service

Provides background server health polling, Windows System Tray integration,
desktop balloon notifications, and quick-action menu controls.
"""

import sys
import os
import time
from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QApplication,
    QStyle
)
from PySide6.QtCore import QObject, QTimer, Signal, Slot
from PySide6.QtGui import QIcon, QAction

from manager.core.api_client import api_client
from manager.core.settings_manager import settings


class HomeLabDaemonSystemTray(QObject):
    """
    Background System Tray Service Daemon for HomeLab OS.
    Runs persistently in system tray to display status, handle notifications,
    and offer quick action shortcuts without keeping full window open.
    """

    status_updated = Signal(dict)
    alert_triggered = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = QApplication.instance()
        self.is_online = False
        self.last_status = None

        # Setup System Tray Icon
        self.tray_icon = QSystemTrayIcon(self._get_default_icon(), parent)
        self.tray_icon.setToolTip("HomeLab OS System Daemon — Initializing...")

        # Setup Context Menu
        self._build_menu()

        # Polling Timer (default: every 10 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_server_status)
        self.poll_interval_ms = settings.get("poll_interval_ms", 10000)

    def _get_default_icon(self) -> QIcon:
        """Returns standard system tray icon fallback."""
        if self.app:
            return self.app.style().standardIcon(QStyle.SP_ComputerIcon)
        return QIcon()

    def _build_menu(self):
        """Builds the context menu attached to system tray icon."""
        self.menu = QMenu()

        self.status_action = QAction("Status: Connecting...", self.menu)
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)
        self.menu.addSeparator()

        self.show_console_action = QAction("Open HomeLab Manager Console", self.menu)
        self.show_console_action.triggered.connect(self.on_open_console)
        self.menu.addAction(self.show_console_action)

        self.lock_vault_action = QAction("Quick Lock LUKS Vault", self.menu)
        self.lock_vault_action.triggered.connect(self.on_quick_lock_vault)
        self.menu.addAction(self.lock_vault_action)

        self.refresh_action = QAction("Refresh Status Now", self.menu)
        self.refresh_action.triggered.connect(self.poll_server_status)
        self.menu.addAction(self.refresh_action)

        self.menu.addSeparator()
        self.quit_action = QAction("Exit HomeLab OS Daemon", self.menu)
        self.quit_action.triggered.connect(self.on_quit)
        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)

    def start(self):
        """Starts system tray daemon and background status timer."""
        self.tray_icon.show()
        self.poll_server_status()
        self.timer.start(self.poll_interval_ms)

    def stop(self):
        """Stops status timer and hides system tray icon."""
        self.timer.stop()
        self.tray_icon.hide()

    @Slot()
    def poll_server_status(self):
        """Polls backend API for status metrics."""
        status = api_client.get_system_status()
        if status:
            self.is_online = True
            self.last_status = status
            cpu = status.get("cpu_percent", 0.0)
            ram = status.get("ram_percent", 0.0)
            server_name = status.get("server_name", "HomeLab OS Node")
            
            tooltip = f"HomeLab OS ({server_name})\nStatus: Online | CPU: {cpu:.1f}% | RAM: {ram:.1f}%"
            self.tray_icon.setToolTip(tooltip)
            self.status_action.setText(f"Online — CPU: {cpu:.1f}% | RAM: {ram:.1f}%")
            self.status_updated.emit(status)
        else:
            self.is_online = False
            self.tray_icon.setToolTip("HomeLab OS — Server Disconnected")
            self.status_action.setText("Status: Offline / Disconnected")
            self.status_updated.emit({"status": "offline"})

    def show_notification(self, title: str, message: str, icon_type=QSystemTrayIcon.Information):
        """Displays native OS desktop notification balloon."""
        if QSystemTrayIcon.supportsMessages():
            self.tray_icon.showMessage(title, message, icon_type, 4000)

    @Slot()
    def on_open_console(self):
        """Callback to raise main window."""
        pass  # Connected by parent window listener

    @Slot()
    def on_quick_lock_vault(self):
        """Quick lock vault from system tray menu."""
        success = api_client.lock_vault()
        if success:
            self.show_notification("LUKS Vault Locked", "Encrypted storage vault was locked successfully.")
        else:
            self.show_notification("Vault Error", "Failed to lock vault or server disconnected.", QSystemTrayIcon.Warning)

    @Slot()
    def on_quit(self):
        """Clean shutdown of daemon."""
        self.stop()
        if self.app:
            self.app.quit()
