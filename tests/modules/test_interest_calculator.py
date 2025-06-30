from modules.module07_interest_calculator.interface import run_module


def test_interest_calculator_basic():
    result = run_module({"action": "test", "data": {}})
    assert isinstance(result, dict)
