from modules.module06_debt_classifier.interface import run_module


def test_debt_classifier_basic():
    result = run_module({"action": "test", "data": {}})
    assert isinstance(result, dict)
