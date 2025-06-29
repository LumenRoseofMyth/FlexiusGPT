# modules/module10_repo_analyzer/interface.py
from pydantic import BaseModel

from .module10_repo_analyzer import run_analysis


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)  # validate
    return run_analysis(payload)
