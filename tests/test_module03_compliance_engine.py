import importlib


def test_compliance_engine_module_loads():
    mod = importlib.import_module(
        "modules.module03_compliance_engine.interface"
    )
    assert hasattr(
        mod,
        "run_module"
    )
