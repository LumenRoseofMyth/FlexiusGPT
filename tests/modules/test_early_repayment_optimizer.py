from modules.module09_early_repayment_optimizer.interface import run_module


def test_early_repayment_optimizer_basic():
    result = run_module({"action": "test", "data": {}})
    assert isinstance(result, dict)
