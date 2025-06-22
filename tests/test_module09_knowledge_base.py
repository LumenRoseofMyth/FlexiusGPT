import importlib


def test_module09_knowledge_base_interface():
    mod = importlib.import_module("modules.module09_knowledge_base.interface")
    assert hasattr(mod, "run_module")
