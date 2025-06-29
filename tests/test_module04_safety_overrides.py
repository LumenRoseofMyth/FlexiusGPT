import importlib


def test_safety_overrides_module_interface():
    mod = importlib.import_module("modules.module04_safety_overrides.interface")
    assert hasattr(mod, "run_module")
