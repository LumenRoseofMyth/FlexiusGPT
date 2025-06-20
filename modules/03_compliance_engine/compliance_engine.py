# Codex Upgrade Timestamp: 2025-06-20T04:09:43.835231Z
"""Compliance Engine module (module_id: 03_compliance_engine)"""

import logging
import os
import yaml

MODULE_ID = "03_compliance_engine"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_module_use(module_id: str, action: str, result: str) -> None:
    """Log module usage in a structured format."""
    logger.info("module=%s action=%s result=%s", module_id, action, result)

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.md")

def load_schema():
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        if lines[0].strip() == '---':
            yaml_lines = []
            for line in lines[1:]:
                if line.strip() == '---':
                    break
                yaml_lines.append(line)
            return yaml.safe_load('\n'.join(yaml_lines))
    return {}

def check_user_compliance(user_log: dict) -> tuple:
    """Validate required compliance events and return status."""

    if not isinstance(user_log, dict):
        raise ValueError("user_log must be a dictionary of compliance flags")

    required = ["session_completed", "feedback_given", "nutrition_logged"]
    missing = [key for key in required if not user_log.get(key, False)]

    if not missing:
        result = (True, "All compliance actions present.")
    else:
        result = (False, f"Missing: {', '.join(missing)}")

    log_module_use(MODULE_ID, "check_user_compliance", result[1])
    return result


module_map = {
    "check_user_compliance": check_user_compliance,
}


if __name__ == "__main__":
    # For local CLI testing
    test_log = {
        "session_completed": True,
        "feedback_given": False,
        "nutrition_logged": True
    }
    print(check_user_compliance(test_log))