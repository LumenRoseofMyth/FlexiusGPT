"""
name: CORE_RULES
description: Rule logic for core compliance
"""
from core.router.validator import validate_payload

@validate_payload
def run_module(*, action: str, test_mode: bool = False, log_path: str | None = None, override_clearance: bool = False) -> dict:
    if action == "test_mode":
        return {
            "success": True,
            "message": "CORE_RULES test_mode executed successfully.",
            "tags": ["core", "rule-check", "test-mode"],
        }
    return {
        "success": True,
        "message": "CORE_RULES executed successfully.",
        "tags": ["core", "rule-check", "test-mode" if test_mode else "run"],
    }
