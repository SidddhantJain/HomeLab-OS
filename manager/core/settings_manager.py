import os
import json

CONFIG_FILE = os.path.expanduser("~/.homelab_manager_config.json")


class SettingsManager:
    """Manages persistent configuration profiles for HomeLab Manager."""
    def __init__(self):
        self.config = {
            "server_ip": "192.168.0.180",
            "server_port": 8000,
            "rdp_port": 3389,
            "username": "media-server",
            "remember_profile": True,
            "auto_connect": True,
            "refresh_interval_sec": 3,
            "dark_mode": True
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"Error loading settings config: {e}")

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving settings config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()


settings = SettingsManager()
