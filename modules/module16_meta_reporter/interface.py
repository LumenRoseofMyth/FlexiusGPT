from pydantic import BaseModel
import os
import json
from datetime import datetime
from modules.module15_deep_repo_orchestrator.interface import run_module as run_orchestrator


class Input(BaseModel):
    action: str
    data: dict


def collect_detailed_repo_data() -> dict:
    repo_data = {}

    for root, dirs, files in os.walk("."):
        root_display = root.replace("\\", "/")
        repo_data[root_display] = []

        for fname in files:
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                size = os.path.getsize(path)
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
                repo_data[root_display].append({
                    "file": fname,
                    "lines": len(lines),
                    "size": size,
                    "modified": mtime,
                })
            except Exception as e:
                repo_data[root_display].append({
                    "file": fname,
                    "error": str(e),
                })

    return repo_data


def run_module(*, payload: dict) -> dict:
    Input(**payload)  # validates payload

    results = {}

    try:
        results["orchestrator"] = run_orchestrator(payload={"action": "deep_scan", "data": {}})
    except Exception as e:
        results["orchestrator"] = {"status": "fail", "error": str(e)}

    try:
        results["repo_analysis"] = collect_detailed_repo_data()
    except Exception as e:
        results["repo_analysis"] = {"status": "fail", "error": str(e)}

    os.makedirs("summaries", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    output_file_txt = f"summaries/meta_report_{timestamp}.txt"
    output_file_json = f"summaries/meta_report_{timestamp}.json"

    with open(output_file_txt, "w", encoding="utf-8") as f:
        for folder, files in results["repo_analysis"].items():
            f.write(f"\n📁 {folder}\n")
            for file_info in files:
                if "error" in file_info:
                    f.write(f"  └── {file_info['file']} ❌ {file_info['error']}\n")
                else:
                    f.write(
                        f"  └── {file_info['file']} "
                        f"(🧮 {file_info['lines']} lines, 📦 {file_info['size']} bytes, 🕓 {file_info['modified']})\n"
                    )

    with open(output_file_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return {
        "status": "complete",
        "output": {
            "txt_file": output_file_txt,
            "json_file": output_file_json,
        },
    }
