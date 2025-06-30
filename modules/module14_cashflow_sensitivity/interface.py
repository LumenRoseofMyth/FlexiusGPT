"""
Module 14 - Cash-Flow Sensitivity Analyzer
Given a baseline monthly income / expenses and a ±percentage delta,
return the resulting final balance over N months.
"""

from typing import Dict

from flexius_monorepo.core.validator import validate_payload


def _simulate(monthly_income: float, monthly_expenses: float, months: int) -> float:
    """Return final balance after `months`."""
    return round((monthly_income - monthly_expenses) * months, 2)


def run_module(payload: Dict) -> Dict:
    """
    Expected envelope:
    {
      "payload": {
        "action": "sensitivity",
        "data": {
          "monthly_income": float,
          "monthly_expenses": float,
          "months": int,
          "delta_pct": float   # e.g. 0.1 → ±10 %
        }
      }
    }
    """
    validate_payload(payload)

    data = payload["payload"]["data"]

    base = _simulate(data["monthly_income"], data["monthly_expenses"], data["months"])
    up_pct = 1 + data["delta_pct"]
    dn_pct = 1 - data["delta_pct"]

    income_up = _simulate(
        data["monthly_income"] * up_pct, data["monthly_expenses"], data["months"]
    )
    income_down = _simulate(
        data["monthly_income"] * dn_pct, data["monthly_expenses"], data["months"]
    )

    expense_up = _simulate(
        data["monthly_income"], data["monthly_expenses"] * up_pct, data["months"]
    )
    expense_down = _simulate(
        data["monthly_income"], data["monthly_expenses"] * dn_pct, data["months"]
    )

    return {
        "status": "ok",
        "baseline": base,
        "income_up": income_up,
        "income_down": income_down,
        "expense_up": expense_up,
        "expense_down": expense_down,
    }
