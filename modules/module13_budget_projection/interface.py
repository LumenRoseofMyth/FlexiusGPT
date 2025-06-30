"""
Module 13 -\nBudget Projection Engine
Takes an income/expense schedule and projects cash-on-hand over N months.
"""

from typing import Dict, List

from flexius_monorepo.core.validator import validate_payload


def _project(
    monthly_income: float, monthly_expenses: List[float], months: int
) -> List[float]:
    balance = 0.0
    curve = []
    for i in range(months):
        balance += monthly_income
        balance -= monthly_expenses[i] if i < len(monthly_expenses) else 0.0
        curve.append(round(balance, 2))
    return curve


def run_module(payload: Dict) -> Dict:
    """
    Expected payload schema
    -----------------------
    {
      "payload": {
        "action": "project",
        "data": {
          "monthly_income": float,
          "monthly_expenses": [float, ...],   # length = months
          "months": int                       # projection horizon
        }
      }
    }
    """
    validate_payload(payload)  # will raise on bad envelope

    data = payload["payload"]["data"]
    curve = _project(
        monthly_income=data["monthly_income"],
        monthly_expenses=data["monthly_expenses"],
        months=data["months"],
    )
    return {
        "status": "ok",
        "projection": curve,
        "final_balance": curve[-1] if curve else 0.0,
    }
