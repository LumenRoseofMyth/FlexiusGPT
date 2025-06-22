# @lock
"""Core payload validator for FlexiusGPT."""
from typing import Dict

def validate_payload(payload: Dict) -> None:
    """Trivial schema validator (Phase 3 placeholder)."""
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")
    if "payload" not in payload:
        raise ValueError("payload missing 'payload' field")
