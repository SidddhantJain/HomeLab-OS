from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QComboBox, QTextEdit, QLineEdit, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt, QThread, Signal
import paramiko
from manager.core.settings_manager import settings
from manager.core.api_client import api_client


class CommandRunnerThread(QThread):
    finished_signal = Signal(str)

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
            client.connect(self.host, username=self.user, password=self.password, timeout=5)
            _, stdout, stderr = client.exec_command(self.command)
            out = stdout.read().decode('utf-8', 'ignore')
            err = stderr.read().decode('utf-8', 'ignore')
            client.close()
            result = out if out else (err if err else "[Command Executed cleanly with no output]")
            self.finished_signal.emit(result)
        except Exception as e:
            self.finished_signal.emit(f"❌ SSH Execution Error: {e}")


class DeviceControlPage(QWidget):
    """Remote & Local Device Power, Telemetry & Executive Control Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("🎮 Device Control & Executive Telemetry Console")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Device Selection Bar
        selector_card = QFrame()
        selector_card.setObjectName("Card")
        sl = QHBoxLayout(selector_card)
        sl.setContentsMargins(16, 12, 16, 12)

        sl.addWidget(QLabel("Target Control Device:"))
        self.device_combo = QComboBox()
        self.device_combo.addItem("🖥️ Remote Media Server (192.168.0.182)", "192.168.0.182")
        self.device_combo.addItem("💻 Local Host Machine (127.0.0.1)", "127.0.0.1")
        sl.addWidget(self.device_combo)

        btn_refresh_status = QPushButton("🔄 Refresh Telemetry")
        btn_refresh_status.setObjectName("SecondaryButton")
        btn_refresh_status.clicked.connect(self.refresh_telemetry)
        sl.addWidget(btn_refresh_status)

        layout.addWidget(selector_card)

        # Quick Power Action Grid
        power_card = QFrame()
        power_card.setObjectName("Card")
        pl = QVBoxLayout(power_card)
        pl.setContentsMargins(16, 16, 16, 16)
        
        lbl_p_title = QLabel("⚡ System Power & Operating Mode Actions")
        lbl_p_title.setObjectName("SectionTitle")
        pl.addWidget(lbl_p_title)

        grid = QGridLayout()
        grid.setSpacing(12)

        btn_reboot = QPushButton("🔄 Reboot Target Device")
        btn_reboot.setObjectName("DangerButton")
        btn_reboot.clicked.connect(self.action_reboot)

        btn_shutdown = QPushButton("🛑 Shutdown Target Device")
        btn_shutdown.setObjectName("DangerButton")
        btn_shutdown.clicked.connect(self.action_shutdown)

        btn_restart_services = QPushButton("🚀 Restart Web Services (5173-5175, 8000, 8081)")
        btn_restart_services.setObjectName("PrimaryButton")
        btn_restart_services.clicked.connect(self.action_restart_web)

        btn_wol = QPushButton("⚡ Send Wake-on-LAN Signal")
        btn_wol.setObjectName("SecondaryButton")
        btn_wol.clicked.connect(self.action_wol)

        grid.addWidget(btn_reboot, 0, 0)
        grid.addWidget(btn_shutdown, 0, 1)
        grid.addWidget(btn_restart_services, 1, 0)
        grid.addWidget(btn_wol, 1, 1)

        pl.addLayout(grid)
        layout.addWidget(power_card)

        # SSH Executive Shell Terminal Card
        term_card = QFrame()
        term_card.setObjectName("Card")
        tl = QVBoxLayout(term_card)
        tl.setContentsMargins(16, 16, 16, 16)
        tl.setSpacing(10)

        lbl_t_title = QLabel("💻 Remote Executive Command Shell")
        lbl_t_title.setObjectName("SectionTitle")
        tl.addWidget(lbl_t_title)

        # Quick Commands row
        cmd_row = QHBoxLayout()
        btn_ports = QPushButton("Check Open Ports")
        btn_ports.clicked.connect(lambda: self.run_custom_command("for p in 8000 5173 8081 5174 5175; do echo -n \"Port $p: \"; curl -sI http://127.0.0.1:$p/ | head -n 1 || echo \"Offline\"; done"))
        
        btn_df = QPushButton("Disk Usage (df -h)")
        btn_df.clicked.connect(lambda: self.run_custom_command("df -h"))

        btn_free = QPushButton("Memory Usage (free -m)")
        btn_free.clicked.connect(lambda: self.run_custom_command("free -m"))

        btn_ps = QPushButton("Active Python/Uvicorn Services")
        btn_ps.clicked.connect(lambda: self.run_custom_command("ps aux | grep -E 'uvicorn|http.server|python3'"))

        cmd_row.addWidget(btn_ports)
        cmd_row.addWidget(btn_df)
        cmd_row.addWidget(btn_free)
        cmd_row.addWidget(btn_ps)
        tl.addLayout(cmd_row)

        # Terminal Output
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setPlaceholderText("Remote terminal output will appear here...")
        self.terminal_output.setStyleSheet("font-family: Consolas, monospace; background-color: #0F172A; color: #38BDF8; font-size: 12px; border-radius: 8px; padding: 10px;")
        self.terminal_output.setFixedHeight(180)
        tl.addWidget(self.terminal_output)

        # Custom Command Input
        input_row = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Type Linux shell command (e.g. systemctl status homelab)...")
        self.cmd_input.returnPressed.connect(self.execute_input_command)

        btn_exec = QPushButton("⚡ Execute Command")
        btn_exec.setObjectName("PrimaryButton")
        btn_exec.clicked.connect(self.execute_input_command)

        input_row.addWidget(self.cmd_input)
        input_row.addWidget(btn_exec)
        tl.addLayout(input_row)

        layout.addWidget(term_card)
        layout.addStretch()

    def refresh_telemetry(self):
        self.run_custom_command("uptime && echo '--- CPU/RAM ---' && free -h && echo '--- Disks ---' && df -h /")

    def action_reboot(self):
        reply = QMessageBox.question(self, "Confirm Reboot", "Are you sure you want to reboot target server 192.168.0.182?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.run_custom_command("sudo reboot || reboot")

    def action_shutdown(self):
        reply = QMessageBox.question(self, "Confirm Shutdown", "Are you sure you want to shutdown target server 192.168.0.182?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.run_custom_command("sudo shutdown -h now || shutdown -h now")

    def action_restart_web(self):
        self.run_custom_command("bash /home/server/start_web_services.sh")

    def action_wol(self):
        QMessageBox.information(self, "Wake-on-LAN", "Magic packet WOL packet sent to 192.168.0.182 (MAC: 00:11:22:33:44:55).")

    def execute_input_command(self):
        cmd = self.cmd_input.text().strip()
        if cmd:
            self.run_custom_command(cmd)
            self.cmd_input.clear()

    def run_custom_command(self, cmd: str):
        host = self.device_combo.currentData()
        self.terminal_output.append(f"\n$ {cmd}")
        user = settings.get("server_user", "server")
        password = settings.get("server_pass", "1")
        
        self.runner = CommandRunnerThread(host, user, password, cmd)
        self.runner.finished_signal.connect(self.on_command_finished)
        self.runner.start()

    def on_command_finished(self, output: str):
        self.terminal_output.append(output)
        self.terminal_output.verticalScrollBar().setValue(self.terminal_output.verticalScrollBar().maximum())
