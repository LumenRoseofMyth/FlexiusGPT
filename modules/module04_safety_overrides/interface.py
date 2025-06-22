from pydantic import BaseModel, ValidationError

class Input(BaseModel):
    action: str
    data: dict

def run_module(*, payload: dict) -> dict:
    Input(**payload)  # raises ValidationError if invalid
    return {"status": "ok"}
 
