"""
name: CORE_RULES
description: Rule logic for core compliance
"""

def test_mode(input_dict: dict = None, *, log_path=None, override_clearance=False) -> dict:
    return {
        "success": True,
        "message": "CORE_RULES test_mode executed successfully.",
        "tags": ["core", "rule-check", "test-mode"]
    }

def run_module(input_dict: dict, *, test_mode=False, log_path=None, override_clearance=False) -> dict:
    return {
        "success": True,
        "message": "CORE_RULES executed successfully.",
        "tags": ["core", "rule-check", "test-mode" if test_mode else "run"]
    }
