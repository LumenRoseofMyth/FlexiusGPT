from core.router.validator import validate_payload

@validate_payload
def run_module(*, action: str) -> dict:
    if action == "test_mode":
        return {"success": True, "msg": "OK"}
    return {"success": False, "msg": "unknown action"}
