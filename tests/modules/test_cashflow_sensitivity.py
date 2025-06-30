from modules.module14_cashflow_sensitivity.interface import run_module


def test_cashflow_sensitivity_basic():
    payload = {
        "payload": {
            "action": "sensitivity",
            "data": {
                "monthly_income": 4000.0,
                "monthly_expenses": 2500.0,
                "months": 12,
                "delta_pct": 0.1,  # ±10 %
            },
        }
    }
    result = run_module(payload)
    assert result["status"] == "ok"
    # baseline: (4000-2500)*12 = 18 000
    assert result["baseline"] == 18000.0
    # +10 % income → (4400-2500)*12 = 22 800
    assert result["income_up"] == 22800.0
    # -10 % income → (3600-2500)*12 = 13 200
    assert result["income_down"] == 13200.0
