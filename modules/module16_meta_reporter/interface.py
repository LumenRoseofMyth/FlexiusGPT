from pydantic import BaseModel
import importlib
import json
import os
from datetime import datetime


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)

    results = {}

    mod_integrity = importlib.import_module(
        "modules.00_integrity_audit.interface"
    )
    mod_analyzer = importlib.import_module(
        "modules.module10_repo_analyzer.module10_repo_analyzer"
    )
    mod_orchestrator = importlib.import_module(
        "modules.module15_deep_repo_orchestrator.interface"
    )

    results["integrity"] = mod_integrity.run_module(
        {"payload": {"action": "scan", "data": {}}}
    )
    results["repo_analysis"] = mod_analyzer.run_analysis({})
    results["orchestrator"] = mod_orchestrator.run_module(
        payload={"action": "meta", "data": {}}
    )

    out_dir = os.path.join(os.path.dirname(__file__), "summaries")
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_path = os.path.join(out_dir, f"{timestamp}_meta_summary.json")
    txt_path = os.path.join(out_dir, f"{timestamp}_meta_summary.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("📦 Meta Summary\n")
        f.write(f"- Governance: {results['integrity']['status']}\n")
        f.write(
            f"- Analyzer File: {results['repo_analysis']['summary_file']}\n"
        )
        f.write(
            f"- Summary Save: "
            f"{results['orchestrator']['result']['summary_save']['status']}\n"
        )

    return {
        "status": "complete",
        "output": {
            "json_file": os.path.basename(json_path),
            "txt_file": os.path.basename(txt_path),
        },
    }
