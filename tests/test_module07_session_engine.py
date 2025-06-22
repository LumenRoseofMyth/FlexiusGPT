import importlib


def test_module07_session_engine_interface():
    mod = importlib.import_module("modules.module07_session_engine.interface")
    assert hasattr(mod, "run_module")
