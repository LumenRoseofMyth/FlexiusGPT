from modules.module10_consolidation_advisor.interface import run_module


def test_consolidation_advisor_basic():
    result = run_module({"action": "test", "data": {}})
    assert isinstance(result, dict)
