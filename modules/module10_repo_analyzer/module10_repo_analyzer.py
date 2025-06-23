from pydantic import BaseModel
import os
import json

from modules.module11_repo_summaries.interface import (
    run_module as run_summaries,
)
from modules.module16_meta_reporter.interface import (
    run_module as run_meta_report,
)


class Input(BaseModel):
    action: str
    data: dict


def run_analysis(_: dict) -> dict:
    result = {
        "status": "complete",
        "structure": sorted(os.listdir("modules")),
        "root_files": sorted(
            f for f in os.listdir(".")
            if f.endswith(".py") or f.endswith(".md")
        ),
    }

    os.makedirs("summaries", exist_ok=True)
    with open(
        "summaries/repo_analysis_latest.json", "w", encoding="utf-8"
    ) as f:
        json.dump(result, f, indent=2)

    return result


def run_module(*, payload: dict) -> dict:
    validated = Input(**payload)

    if validated.action != "analyze":
        return {
            "status": "error",
            "message": f"Unsupported action: {validated.action}",
        }

    result = run_analysis(validated.data)

    summary_result = run_summaries(
        payload={"action": "summary_report", "data": {}}
    )
    meta_result = run_meta_report(
        payload={"action": "test", "data": {}}
    )

    return {
        "status": "chain_complete",
        "analysis": result,
        "summary": summary_result,
        "meta_report": meta_result,
    }
