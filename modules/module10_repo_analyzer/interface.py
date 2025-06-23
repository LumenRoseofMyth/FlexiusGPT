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


def get_file_tree(base_path="."):
    tree = {}
    for root, dirs, files in os.walk(base_path):
        rel_path = os.path.relpath(root, base_path)
        pointer = tree
        if rel_path != ".":
            for part in rel_path.split(os.sep):
                pointer = pointer.setdefault(part, {})
        pointer["__files__"] = sorted(files)
    return tree


def run_module(*, payload: dict) -> dict:
    validated = Input(**payload)

    if validated.action != "analyze":
        return {
            "status": "error",
            "message": f"Unsupported action: {validated.action}",
        }

    # Generate analysis
    structure = sorted(os.listdir("modules"))
    root_files = sorted(
        f for f in os.listdir(".") if f.endswith(".py") or f.endswith(".md")
    )
    full_tree = get_file_tree()

    result = {
        "status": "complete",
        "structure": structure,
        "root_files": root_files,
        "full_tree": full_tree,
    }

    os.makedirs("summaries", exist_ok=True)
    with open("summaries/repo_analysis_latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # Format summary for Module 11
    summary_text = f"""# Repository Summary

## Modules
{chr(10).join(f"- {mod}" for mod in structure)}

## Root Files
{chr(10).join(f"- {file}" for file in root_files)}
"""

    summary_result = run_summaries(
        payload={"action": "summary_report", "data": {"text": summary_text}}
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
