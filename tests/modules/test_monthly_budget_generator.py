from modules.module12_monthly_budget_generator.interface import run_module


def test_monthly_budget_generator_basic():
    result = run_module({"action": "test", "data": {}})
    assert isinstance(result, dict)
