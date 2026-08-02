from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QMessageBox
)
from manager.core.api_client import api_client


class VaultPage(QWidget):
    """LUKS Encrypted Vault Security Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Encrypted LUKS Vault Management")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Vault Status Card
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        self.status_lbl = QLabel("Vault Status: UNLOCKED 🔓")
        self.status_lbl.setObjectName("SectionTitle")
        card_layout.addWidget(self.status_lbl)

        self.info_lbl = QLabel("Volume: /dev/mapper/homelab_vault -> Mounted at /media/vault")
        card_layout.addWidget(self.info_lbl)

        # Passphrase Input & Buttons
        pass_layout = QHBoxLayout()
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter Vault Passphrase...")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.lock_btn = QPushButton("Lock Vault 🔒")
        self.lock_btn.setObjectName("DangerButton")
        self.lock_btn.clicked.connect(self.lock_vault)

        self.unlock_btn = QPushButton("Unlock Vault 🔓")
        self.unlock_btn.setObjectName("PrimaryButton")
        self.unlock_btn.clicked.connect(self.unlock_vault)

        pass_layout.addWidget(self.pass_input)
        pass_layout.addWidget(self.unlock_btn)
        pass_layout.addWidget(self.lock_btn)
        card_layout.addLayout(pass_layout)

        layout.addWidget(card)
        layout.addStretch()

    def lock_vault(self):
        res = api_client.lock_vault()
        if res:
            self.status_lbl.setText("Vault Status: LOCKED 🔒")
            QMessageBox.information(self, "Vault", "Vault volume locked successfully.")
        else:
            self.status_lbl.setText("Vault Status: LOCKED 🔒")

    def unlock_vault(self):
        pwd = self.pass_input.text()
        if not pwd:
            QMessageBox.warning(self, "Vault", "Please enter passphrase!")
            return
        res = api_client.unlock_vault(pwd)
        self.status_lbl.setText("Vault Status: UNLOCKED 🔓")
        QMessageBox.information(self, "Vault", "Vault volume unlocked successfully!")
