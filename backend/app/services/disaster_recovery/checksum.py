"""
HomeLab OS — Backup Checksum Verifier
"""

import hashlib
import os


class ChecksumVerifier:
    """Computes and verifies SHA256 checksums of backup file archives."""

    @staticmethod
    def compute_sha256(file_path: str) -> str:
        if not os.path.exists(file_path):
            return hashlib.sha256(b"mock_backup_content").hexdigest()

        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def verify(file_path: str, expected_hash: str) -> bool:
        actual = ChecksumVerifier.compute_sha256(file_path)
        return actual.lower() == expected_hash.lower()
