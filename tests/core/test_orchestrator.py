import pytest
from core.orchestrator import (
    CorePermissionError,
    PayloadValidationError,
    call_module_logic,
)


def test_core_protection_enforced():
    protected = "core.test"
    payload = {"payload": {"action": "noop", "data": {}}}
    with pytest.raises(CorePermissionError):
        call_module_logic(protected, payload)


def test_invalid_schema_raises():
    with pytest.raises(PayloadValidationError):
        call_module_logic("module01", {"payload": {"action": "x"}})
