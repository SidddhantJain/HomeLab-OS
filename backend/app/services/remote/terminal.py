"""
HomeLab OS — Remote Terminal Sandbox
"""

from typing import Dict, Any, List


class TerminalSandbox:
    """Provides a controlled execution sandbox for the remote web terminal."""

    FORBIDDEN_PATTERNS = ["rm -rf /", "mkfs", "dd if=", ":(){ :|:& };:"]

    def execute_terminal_command(self, raw_command: str) -> Dict[str, Any]:
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in raw_command:
                return {
                    "command": raw_command,
                    "error": "Forbidden command pattern detected.",
                    "status": "REJECTED"
                }

        return {
            "command": raw_command,
            "output": f"homelab-shell$ {raw_command}\n[Command output processed in sandbox environment]",
            "status": "SUCCESS"
        }
