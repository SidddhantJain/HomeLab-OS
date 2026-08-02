import requests
import json
from manager.core.settings_manager import settings


class APIClient:
    """REST API Client for communicating with HomeLab OS FastAPI Backend."""
    def __init__(self):
        self.auth_token = None

    @property
    def base_url(self) -> str:
        ip = settings.get("server_ip", "192.168.0.180")
        port = settings.get("server_port", 8000)
        return f"http://{ip}:{port}/api/v1"

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def get_system_status(self):
        try:
            r = requests.get(f"{self.base_url}/system/status", headers=self._headers(), timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"API Error (system/status): {e}")
        return None

    def get_devices(self):
        try:
            r = requests.get(f"{self.base_url}/network/devices", headers=self._headers(), timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"API Error (network/devices): {e}")
        return []

    def get_containers(self):
        try:
            r = requests.get(f"{self.base_url}/docker/containers", headers=self._headers(), timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"API Error (docker/containers): {e}")
        return []

    def get_storage(self):
        try:
            r = requests.get(f"{self.base_url}/system/storage", headers=self._headers(), timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"API Error (system/storage): {e}")
        return None

    def get_vault_status(self):
        try:
            r = requests.get(f"{self.base_url}/vault/status", headers=self._headers(), timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"API Error (vault/status): {e}")
        return None

    def lock_vault(self):
        try:
            r = requests.post(f"{self.base_url}/vault/lock", headers=self._headers(), timeout=5)
            return r.status_code == 200
        except Exception as e:
            print(f"API Error (vault/lock): {e}")
        return False

    def unlock_vault(self, passphrase: str):
        try:
            r = requests.post(
                f"{self.base_url}/vault/unlock",
                json={"passphrase": passphrase},
                headers=self._headers(),
                timeout=5
            )
            return r.status_code == 200
        except Exception as e:
            print(f"API Error (vault/unlock): {e}")
        return False


api_client = APIClient()
