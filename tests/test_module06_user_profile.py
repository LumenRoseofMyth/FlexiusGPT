import importlib


def test_module06_user_profile_interface():
    mod = importlib.import_module("modules.module06_user_profile.interface")
    assert hasattr(mod, "run_module")
