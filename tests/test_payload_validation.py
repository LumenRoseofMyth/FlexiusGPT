import pytest
from importlib import import_module
from fastapi import HTTPException

from adapters.gpt_adapter import call_module_logic

mod = import_module("modules.01_core_rules.core_rules")


def test_run_module_requires_payload():
    with pytest.raises(TypeError):
        mod.run_module(action="test_mode")


def test_call_module_logic_success():
    result = call_module_logic("01_core_rules", {"action": "test_mode", "test_mode": True})
    assert result["success"] is True


def test_call_module_logic_schema_error():
    with pytest.raises(HTTPException) as exc:
        call_module_logic("01_core_rules", {"foo": "bar"})
    assert exc.value.status_code == 422
    detail = exc.value.detail
    assert "expected_schema" in detail
    assert "received_payload" in detail
