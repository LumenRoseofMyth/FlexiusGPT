import importlib


def test_module08_feedback_engine_interface():
    mod = importlib.import_module("modules.module08_feedback_engine.interface")
    assert hasattr(mod, "run_module")
