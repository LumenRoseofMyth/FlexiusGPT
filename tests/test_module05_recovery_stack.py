import importlib


def test_module05_recovery_stack_interface():
    mod = importlib.import_module("modules.module05_recovery_stack.interface")
    assert hasattr(mod, "run_module")
