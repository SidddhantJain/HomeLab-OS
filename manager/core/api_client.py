import requests
import json
import time
from manager.core.settings_manager import settings


class APIClient:
    """REST API Client for communicating with HomeLab OS FastAPI Backend."""
    def __init__(self):
        self.auth_token = None
        self.last_status_cache = None
        self.last_check_time = 0
        self.is_reachable = False

    @property
    def base_url(self) -> str:
        ip = settings.get("server_ip", "192.168.0.182")
        port = settings.get("server_port", 8000)
        return f"http://{ip}:{port}/api/v1"

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def check_connection(self, timeout=0.5) -> bool:
        """Fast non-blocking connection check."""
        try:
            r = requests.get(f"{self.base_url}/system/status", headers=self._headers(), timeout=timeout)
            self.is_reachable = (r.status_code == 200)
            if self.is_reachable:
                self.last_status_cache = r.json()
                self.last_check_time = time.time()
            return self.is_reachable
        except Exception:
            self.is_reachable = False
            return False

    def get_system_status(self, timeout=0.5):
        try:
            r = requests.get(f"{self.base_url}/system/status", headers=self._headers(), timeout=timeout)
            if r.status_code == 200:
                self.last_status_cache = r.json()
                self.is_reachable = True
                return self.last_status_cache
        except Exception as e:
            self.is_reachable = False
        return None

    def get_devices(self, timeout=0.5):
        try:
            r = requests.get(f"{self.base_url}/network/devices", headers=self._headers(), timeout=timeout)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            pass
        return []

    def get_containers(self, timeout=0.5):
        try:
            r = requests.get(f"{self.base_url}/docker/containers", headers=self._headers(), timeout=timeout)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            pass
        return []

    def get_storage(self, timeout=0.5):
        try:
            r = requests.get(f"{self.base_url}/system/storage", headers=self._headers(), timeout=timeout)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            pass
        return None

    def get_vault_status(self, timeout=0.5):
        try:
            r = requests.get(f"{self.base_url}/vault/status", headers=self._headers(), timeout=timeout)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            pass
        return None

    def lock_vault(self, timeout=0.5):
        try:
            r = requests.post(f"{self.base_url}/vault/lock", headers=self._headers(), timeout=timeout)
            return r.status_code == 200
        except Exception as e:
            pass
        return False

    def unlock_vault(self, passphrase: str, timeout=0.5):
        try:
            r = requests.post(
                f"{self.base_url}/vault/unlock",
                json={"passphrase": passphrase},
                headers=self._headers(),
                timeout=timeout
            )
            return r.status_code == 200
        except Exception as e:
            pass
        return False


api_client = APIClient()

