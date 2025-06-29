from pydantic import BaseModel


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)  # raises ValidationError if invalid
    return {"status": "compliance_engine_stub_ran", "payload": payload}
