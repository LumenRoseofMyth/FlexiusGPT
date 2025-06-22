import importlib

def test_core_rules_module_naming():
    mod = importlib.import_module("modules.module01_core_rules.interface")
    result = mod.run_module(payload={"action": "enforce", "data": {}})

    assert isinstance(result, dict)
    assert "issues" in result
    assert "missing_interface" in result["issues"]
    assert "missing_run_module" in result["issues"]
    assert "missing_lock" in result["issues"]
    assert "missing_init" in result["issues"]
