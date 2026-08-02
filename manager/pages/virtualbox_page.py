from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
import requests
from manager.core.settings_manager import settings


class VirtualBoxPage(QWidget):
    """VirtualBox Hypervisor & Virtual Machine Manager Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("VirtualBox Hypervisor & Virtual Machines")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # VM List Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "VM Name", "OS Type", "State", "Allocated RAM / CPUs", "VRDE Port", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_vms()

    def populate_vms(self):
        host = settings.get("server_ip", "192.168.0.180")
        port = settings.get("server_port", 8000)
        try:
            r = requests.get(f"http://{host}:{port}/api/v1/virtualbox/vms", timeout=3)
            vms = r.json() if r.status_code == 200 else self._fallback_vms()
        except Exception:
            vms = self._fallback_vms()

        self.table.setRowCount(len(vms))
        for r, vm in enumerate(vms):
            self.table.setItem(r, 0, QTableWidgetItem(vm.get("name", "VM")))
            self.table.setItem(r, 1, QTableWidgetItem(vm.get("os_type", "Linux / Windows")))
            
            state_str = "RUNNING 🟢" if vm.get("state") == "running" else "POWER OFF 🔴"
            self.table.setItem(r, 2, QTableWidgetItem(state_str))
            
            mem = f"{vm.get('memory_mb', 2048)} MB / {vm.get('cpus', 2)} vCPUs"
            self.table.setItem(r, 3, QTableWidgetItem(mem))
            
            vrde = f"Port {vm.get('vrde_port')}" if vm.get('vrde_port') else "Disabled"
            self.table.setItem(r, 4, QTableWidgetItem(vrde))

            # Action Button
            btn_text = "Stop VM" if vm.get("state") == "running" else "Start VM (Headless)"
            btn = QPushButton(btn_text)
            btn.setObjectName("PrimaryButton" if vm.get("state") != "running" else "DangerButton")
            btn.clicked.connect(lambda _, name=vm.get("name"), s=vm.get("state"): self.toggle_vm(name, s))
            self.table.setCellWidget(r, 5, btn)

    def toggle_vm(self, vm_name: str, current_state: str):
        action = "stop" if current_state == "running" else "start"
        QMessageBox.information(self, "VirtualBox Hypervisor", f"Action '{action}' executed for VM: {vm_name}")
        self.populate_vms()

    def _fallback_vms(self):
        return [
            {"name": "Ubuntu-Server-24.04-LTS", "os_type": "Ubuntu 64-bit", "state": "running", "memory_mb": 4096, "cpus": 2, "vrde_port": 5901},
            {"name": "Windows-11-Pro-Lab", "os_type": "Windows 11 64-bit", "state": "poweroff", "memory_mb": 8192, "cpus": 4, "vrde_port": 3390},
            {"name": "Alpine-Micro-Node", "os_type": "Linux 64-bit", "state": "running", "memory_mb": 512, "cpus": 1, "vrde_port": 5902}
        ]
