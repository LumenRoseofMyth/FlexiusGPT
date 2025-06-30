from core.validator import validate_payload


def run_module(payload: dict) -> dict:
    validate_payload({"payload": payload})
    return {"status": "ok"}
