import importlib

def test_phase_manager_module_exists():
    mod = importlib.import_module("modules.module02_phase_manager.interface")
    assert hasattr(mod, "run_module")
