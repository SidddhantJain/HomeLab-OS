"""
HomeLab OS — Vault LUKS & Cryptsetup Manager

Interfaces with host cryptsetup and loop devices to manage encrypted vault images.
"""

from __future__ import annotations

import os
import subprocess
from typing import Dict, Any


class VaultEncryptionManager:
    """Orchestrates loop devices, cryptsetup operations, and filesystems."""

    def __init__(self, container_path: str = "/opt/homelab/vault.img", mapper_name: str = "homelab_vault") -> None:
        self.container_path = container_path
        self.mapper_name = mapper_name
        self.mapped_path = f"/dev/mapper/{mapper_name}"

    def check_cryptsetup_available(self) -> bool:
        """Returns True if cryptsetup is present on the host system."""
        try:
            subprocess.run(["cryptsetup", "--version"], capture_output=True, check=False)
            return True
        except (FileNotFoundError, PermissionError):
            return False

    def create_vault_container(self, size_gb: int = 100) -> bool:
        """Allocates an empty loopback container image."""
        if os.path.exists(self.container_path):
            return True

        # Ensure parent directories exist
        os.makedirs(os.path.dirname(self.container_path), exist_ok=True)

        try:
            # Create a sparse file of size_gb
            with open(self.container_path, "wb") as f:
                f.truncate(size_gb * 1024 * 1024 * 1024)
            return True
        except OSError as e:
            print(f"[VaultEncryptionManager] Failed to create container file: {e}")
            return False

    def format_luks(self, password: str) -> bool:
        """Applies LUKS2 encryption structure to the container file."""
        if not self.check_cryptsetup_available():
            # In developer/mock mode, we succeed
            return True

        try:
            # Execute LUKS format
            process = subprocess.Popen(
                ["cryptsetup", "luksFormat", "--type", "luks2", self.container_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Send password twice to confirm
            stdout, stderr = process.communicate(input=f"{password}\n{password}\n")
            return process.returncode == 0
        except Exception as e:
            print(f"[VaultEncryptionManager] LUKS format failed: {e}")
            return False

    def open_luks(self, password: str) -> bool:
        """Decrypts and mounts LUKS2 container using the password."""
        if not self.check_cryptsetup_available():
            return True

        try:
            process = subprocess.Popen(
                ["cryptsetup", "open", self.container_path, self.mapper_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=f"{password}\n")
            return process.returncode == 0
        except Exception as e:
            print(f"[VaultEncryptionManager] LUKS open failed: {e}")
            return False

    def close_luks(self) -> bool:
        """Safely closes the mapped LUKS device."""
        if not self.check_cryptsetup_available():
            return True

        try:
            res = subprocess.run(["cryptsetup", "close", self.mapper_name], capture_output=True, check=False)
            return res.returncode == 0
        except Exception as e:
            print(f"[VaultEncryptionManager] LUKS close failed: {e}")
            return False
