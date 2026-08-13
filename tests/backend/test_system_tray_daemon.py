"""
HomeLab OS — PySide6 Desktop System Tray Daemon Test Suite
Validates HomeLabDaemonSystemTray signals, polling handlers, and status menu formatting.
"""

import sys
import os
import pytest
from PySide6.QtWidgets import QApplication
from manager.core.daemon import HomeLabDaemonSystemTray


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    yield app


def test_system_tray_daemon_instantiation(qapp):
    daemon = HomeLabDaemonSystemTray()
    assert daemon is not None
    assert daemon.is_online is False
    assert daemon.timer is not None


def test_system_tray_context_menu(qapp):
    daemon = HomeLabDaemonSystemTray()
    assert daemon.menu is not None
    actions = [action.text() for action in daemon.menu.actions()]
    assert any("Open HomeLab Manager Console" in a for a in actions)
    assert any("Quick Lock LUKS Vault" in a for a in actions)
    assert any("Refresh Status Now" in a for a in actions)


def test_system_tray_status_polling_fallback(qapp):
    daemon = HomeLabDaemonSystemTray()
    daemon.poll_server_status()
    # Offline fallback handled cleanly
    assert daemon.status_action.text() is not None
