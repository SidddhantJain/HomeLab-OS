import sys
import os
import signal
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from manager.launcher import ServerLauncherDialog
from manager.main_window import HomeLabMainWindow
from manager.core.daemon import HomeLabDaemonSystemTray


def load_stylesheet(app: QApplication):
    qss_path = os.path.join(os.path.dirname(__file__), "themes", "dark_theme.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


def main():
    # Enable High DPI scaling & crisp font rendering
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("HomeLab OS Manager")
    app.setOrganizationName("HomeLab OS")
    app.setStyle("Fusion")
    load_stylesheet(app)

    # Initialize System Tray Daemon
    daemon = HomeLabDaemonSystemTray()

    # Launch server connection dialog
    launcher = ServerLauncherDialog()
    if launcher.exec() == ServerLauncherDialog.Accepted:
        window = HomeLabMainWindow()
        
        # Connect System Tray "Open Console" action to main window raise/activate
        daemon.on_open_console = lambda: (
            window.showNormal() if window.isMinimized() else None,
            window.show(),
            window.activateWindow()
        )
        
        daemon.start()
        window.show()
        
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

