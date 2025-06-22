import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "api" / ".well-known"
PLUGIN_FILE = BASE / "ai-plugin.json"

def update_manifest(base_url: str):
    with PLUGIN_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data["api"]["url"] = f"{base_url}/openapi.json"
    data["logo_url"] = f"{base_url}/logo.png"
    data["legal_info_url"] = f"{base_url}/legal"
    with PLUGIN_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

if __name__ == "__main__":
    url = os.environ.get("CONNECTOR_PUBLIC_URL", "http://localhost:8000")
    update_manifest(url)
