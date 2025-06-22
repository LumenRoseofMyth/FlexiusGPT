# @lock
"""
Payload schema and validator for FlexiusGPT.
"""
from jsonschema import validate, ValidationError

SCHEMA = {
    "type": "object",
    "properties": {
        "payload": {
            "type": "object",
            "properties": {
                "action": {"type": "string"},
                "data": {"type": "object"}
            },
            "required": ["action", "data"]
        }
    },
    "required": ["payload"],
    "additionalProperties": False
}

def validate_payload(payload: dict) -> None:
    """Validate payload or raise ValueError."""
    try:
        validate(instance=payload, schema=SCHEMA)
    except ValidationError as exc:
        raise ValueError(f"Invalid payload: {exc.message}") from None
