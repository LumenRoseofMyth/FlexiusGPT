import pytest
from importlib import import_module
from fastapi import HTTPException

from adapters.gpt_adapter import call_module_logic

mod = import_module("modules.01_core_rules.core_rules")

def test_run_module_requires_payload() -> None:
    """run_module should raise TypeError if called without payload kwarg."""
    with pytest.raises(TypeError):
        mod.run_module(action="test_mode")

def test_call_module_logic_success():
    """call_module_logic should succeed with valid payload."""
    result = call_module_logic("01_core_rules", {"action": "test_mode"})
    assert result["success"] is True, "Expected success for valid action"

def test_call_module_logic_schema_error():
    """call_module_logic should raise HTTPException for invalid payload."""
    with pytest.raises(HTTPException) as exc_info:
        call_module_logic("01_core_rules", {"foo": "bar"})
    exc: HTTPException = exc_info.value
    assert getattr(exc, "status_code", None) == 422, "Expected 422 for schema error"
    detail = exc.detail
    assert "expected_schema" in detail, "Missing expected_schema in error detail"
    assert "received_payload" in detail, "Missing received_payload in error detail"