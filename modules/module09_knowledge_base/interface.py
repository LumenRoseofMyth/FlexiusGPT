from pydantic import BaseModel


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)
    return {"status": "ok", "module": "knowledge_base"}
