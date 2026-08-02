from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLineEdit, QPushButton, QLabel, QTabWidget
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
import paramiko


class SSHWorker(QThread):
    output_received = Signal(str)

    def __init__(self, host, user, password, command):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.command = command

    def run(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.host, port=22, username=self.user, password=self.password, timeout=5)
            stdin, stdout, stderr = client.exec_command(self.command)
            out = stdout.read().decode("utf-8", errors="replace")
            err = stderr.read().decode("utf-8", errors="replace")
            res = out if out else err
            self.output_received.emit(res)
            client.close()
        except Exception as e:
            self.output_received.emit(f"SSH Error: {e}")


class RemoteTerminalWidget(QWidget):
    """Tabbed SSH Console & Command Execution Terminal Widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Output Terminal View
        self.console_output = QPlainTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setFont(QFont("Consolas", 10))
        self.console_output.setStyleSheet("background-color: #090D16; color: #38BDF8; border: 1px solid #334155; border-radius: 8px;")
        self.console_output.appendPlainText("Welcome to HomeLab OS Remote SSH Terminal Console\nConnected to media-server@192.168.0.180:22\nType command below and press Enter (or click Send):\n" + "-"*60 + "\n")

        # Input Command Row
        cmd_row = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command (e.g., uname -a, htop, docker ps)...")
        self.cmd_input.returnPressed.connect(self.send_command)

        self.send_btn = QPushButton("Execute ➔")
        self.send_btn.setObjectName("PrimaryButton")
        self.send_btn.clicked.connect(self.send_command)

        cmd_row.addWidget(self.cmd_input)
        cmd_row.addWidget(self.send_btn)

        layout.addWidget(self.console_output)
        layout.addLayout(cmd_row)

    def send_command(self):
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return

        self.console_output.appendPlainText(f"\nmedia-server@192.168.0.180:~$ {cmd}")
        self.cmd_input.clear()

        # Run SSH in background thread to avoid freezing UI
        self.worker = SSHWorker("192.168.0.180", "media-server", "1", cmd)
        self.worker.output_received.connect(self.on_output)
        self.worker.start()

    def on_output(self, text):
        self.console_output.appendPlainText(text)
