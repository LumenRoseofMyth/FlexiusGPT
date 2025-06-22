from core.router.validator import validate_payload

from typing import Dict, Any

@validate_payload
def run_module(*, action: str) -> Dict[str, Any]:
    if action == "test_mode":
        return {"success": True, "msg": "OK"}
    return {"success": False, "msg": "unknown action"}
