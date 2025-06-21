from modules.core.io.code_reflector import summarize_codex_diff
from modules.core.io.connector import get_active_connector_url


def dispatch_query(topic):
    if topic == "codex-diff":
        return summarize_codex_diff("UPGRADE.md")
    elif topic == "connector-status":
        return get_active_connector_url() or "No valid connector online."
    return "Unknown topic."
