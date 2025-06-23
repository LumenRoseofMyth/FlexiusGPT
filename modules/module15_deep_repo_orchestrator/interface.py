from pydantic import BaseModel
import importlib


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)

    results = {}

    # Run governance audit
    mod_integrity = importlib.import_module(
        "modules.00_integrity_audit.interface"
    )
    results["governance"] = mod_integrity.run_module(
        {"payload": {"action": "scan", "data": {}}}
    )

    # Run repo analyzer
    mod_analyzer = importlib.import_module(
        "modules.module10_repo_analyzer.module10_repo_analyzer"
    )
    results["repo_analysis"] = mod_analyzer.run_analysis({})

    # Save summary using module11
    mod_saver = importlib.import_module(
        "modules.module11_repo_summaries.interface"
    )
    text = (
        "📦 Governance: "
        + results["governance"]["status"]
        + "\n\n📊 Analyzer Output Saved: "
        + results["repo_analysis"]["summary_file"]
    )
    results["summary_save"] = mod_saver.run_module(
        payload={"action": "deep_repo_summary", "data": {"text": text}}
    )

    return {"status": "complete", "result": results}
