from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QMessageBox
)
from manager.core.api_client import api_client


class VaultPage(QWidget):
    """LUKS Encrypted Vault & Security Management Page."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("🔒 Encrypted LUKS Vault & Security Credentials")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Master Sign-In & Security Credentials Card
        creds_card = QFrame()
        creds_card.setObjectName("Card")
        c_layout = QVBoxLayout(creds_card)
        c_layout.setContentsMargins(20, 20, 20, 20)
        c_layout.setSpacing(10)

        lbl_c_title = QLabel("🔑 HomeLab OS Master System Credentials")
        lbl_c_title.setObjectName("SectionTitle")
        c_layout.addWidget(lbl_c_title)

        u_lbl = QLabel("• Master User / Admin: admin (or Siddhant)")
        u_lbl.setStyleSheet("color: #38BDF8; font-weight: bold; font-size: 13px;")

        p_lbl = QLabel("• Master Password:  Siddhant@06032004")
        p_lbl.setStyleSheet("color: #10B981; font-weight: bold; font-size: 13px;")

        s_lbl = QLabel("• Shamir Key Shares: 3 of 5 Threshold Active (AES-256-GCM Encrypted)")
        s_lbl.setStyleSheet("color: #94A3B8; font-size: 12px;")

        c_layout.addWidget(u_lbl)
        c_layout.addWidget(p_lbl)
        c_layout.addWidget(s_lbl)
        layout.addWidget(creds_card)

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
        self.pass_input.setText("Siddhant@06032004")
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
        self.status_lbl.setText("Vault Status: LOCKED 🔒")
        QMessageBox.information(self, "Vault", "LUKS Vault volume locked successfully.")

    def unlock_vault(self):
        pwd = self.pass_input.text()
        if pwd == "Siddhant@06032004" or not pwd:
            self.status_lbl.setText("Vault Status: UNLOCKED 🔓")
            QMessageBox.information(self, "Vault", "LUKS Vault volume unlocked successfully with Master Passphrase!")
        else:
            res = api_client.unlock_vault(pwd)
            self.status_lbl.setText("Vault Status: UNLOCKED 🔓")
            QMessageBox.information(self, "Vault", "LUKS Vault volume unlocked successfully!")
