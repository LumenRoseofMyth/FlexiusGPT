import json
import re
from pathlib import Path
import httpx

CONFIG_PATH = Path("connector_config.json")


def _poll_ngrok_url() -> str | None:
    """Return the public https URL from the local ngrok API."""
    try:
        resp = httpx.get("http://127.0.0.1:4040/api/tunnels", timeout=2)
        resp.raise_for_status()
        data = resp.json()
        for t in data.get("tunnels", []):
            if t.get("proto") == "https":
                return t.get("public_url")
    except Exception:
        pass
    return None


def refresh_connector_config() -> None:
    """Update connector_config.json with current ngrok URL if changed."""
    if not CONFIG_PATH.exists():
        return
    new_url = _poll_ngrok_url()
    if not new_url:
        return
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    if config.get("url") != new_url:
        config["url"] = new_url
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)


def get_active_connector_url():
    if not CONFIG_PATH.exists():
        return None
    refresh_connector_config()
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    url = config.get("url")
    enabled = config.get("enabled", False)
    if enabled and url and re.match(r"https://[a-z0-9-]+.ngrok-free.app", url):
        return url
    return None
