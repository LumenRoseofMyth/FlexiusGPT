# tests/test_module10_repo_analyzer.py
import importlib

def test_module10_repo_analyzer():
    mod = importlib.import_module("modules.module10_repo_analyzer.interface")
    assert hasattr(mod, "run_module")
