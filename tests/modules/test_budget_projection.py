from modules.module13_budget_projection.interface import run_module


def test_budget_projection_basic():
    payload = {
        "payload": {
            "action": "project",
            "data": {
                "monthly_income": 5000.0,
                "monthly_expenses": [3000.0] * 6,
                "months": 6,
            },
        }
    }
    result = run_module(payload)
    assert result["status"] == "ok"
    assert len(result["projection"]) == 6
    assert result["projection"][-1] == 12000.0  # 2000 surplus × 6
