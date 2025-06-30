from typing import Any, Dict

from pydantic import BaseModel, model_validator


class PayloadModel(BaseModel):
    action: str
    data: Dict[str, Any]

    @model_validator(mode="before")
    def check_no_extra_fields(cls, values):
        extra_keys = set(values.keys()) - {"action", "data"}
        if extra_keys:
            raise ValueError(f"Unexpected fields in payload: {extra_keys}")
        return values


class Envelope(BaseModel):
    payload: PayloadModel

    @model_validator(mode="before")
    def check_no_extra_fields(cls, values):
        extra_keys = set(values.keys()) - {"payload"}
        if extra_keys:
            raise ValueError(f"Unexpected fields in envelope: {extra_keys}")
        return values


def validate_payload(input_data: Dict[str, Any]) -> None:
    """
    Validate the incoming data structure.
    Raises ValueError if unexpected keys or missing fields are found.
    """
    Envelope(**input_data)
