# modules/module02_phase_manager/interface.py
from pydantic import BaseModel


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)  # raises ValidationError if invalid
    action = payload["action"]

    if action == "get_phase":
        return {"phase": "initial"}
    elif action == "advance_phase":
        return {"phase": "next"}
    else:
        return {"error": f"Unknown action: {action}"}
