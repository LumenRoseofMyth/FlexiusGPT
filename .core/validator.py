from typing import Any, Dict

from jsonschema import ValidationError, validate

SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "payload": {
            "type": "object",
            "properties": {
                "action": {"type": "string"},
                "data": {"type": "object"},
            },
            "required": ["action", "data"],
        }
    },
    "required": ["payload"],
    "additionalProperties": False,
}


def validate_payload(payload: Dict[str, Any]) -> None:
    """Validate payload or raise ValueError."""
    try:
        validate(instance=payload, schema=SCHEMA)
    except ValidationError as exc:  # pragma: no cover
        raise ValueError(f"Invalid payload: {exc.message}") from None
