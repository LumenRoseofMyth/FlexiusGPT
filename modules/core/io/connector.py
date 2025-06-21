import json
import re
from pathlib import Path

CONFIG_PATH = Path("connector_config.json")


def get_active_connector_url():
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    url = config.get("url")
    enabled = config.get("enabled", False)
    if enabled and url and re.match(r"https://[a-z0-9-]+.ngrok-free.app", url):
        return url
    return None
