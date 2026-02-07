import json 
from pathlib import Path 

CONFIG_FILE = Path("./config.json")

class Settings:
    def __init__(self):
        self._config: dict[str,None|str|int] = {
            "default_asset": "BTCUSDT",
            "default_timeframe": "15",
            "automation_status": None,
            "user": "HUMAN OVERLORD",
        }
        self.load()


    def load(self): 
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                try:
                    self._config.update(json.load(f))
                except json.JSONDecodeError:
                    print("Warning: Config file is corrupted, using default settings")
                    self.save()
        else:
            self.save()


    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self._config, f, indent=4)


    def get(self, key, default=None):
        return self._config.get(key, default)


    def set(self, key, value):
        self._config[key] = value
        self.save()


    # GETTERS
    def username(self) -> str:
        return str(self._config.get("user"))


    def asset(self) -> str:
        val = self._config.get("default_asset")
        if val is None or isinstance(val, int):
            print("Asset is set to None in config")
            return ""

        return val


    def timeframe(self) -> str:
        val = self._config.get("default_timeframe")
        if val is None or isinstance(val, int):
            print("Timeframe is set to None in config")
            return ""

        return val


    def automation_status(self):
        val = self._config.get("automation_status")
        return val


    # SETTERS / SAVEERS
    # Could be generalized to single function call
    def save_username(self, value):
        self._config["user"] = value
        self.save()


    def save_asset(self, value):
        self._config["default_asset"] = value
        self.save()


    def save_timeframe(self, value):
        self._config["default_timeframe"] = value 
        self.save()


    def save_automation_status(self, value):
        self._config["automation_status"] = value 
        self.save()
