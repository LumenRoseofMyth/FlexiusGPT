# modules/module10_repo_analyzer/module10_repo_analyzer.py
import os
from datetime import datetime

REPORT_PATH = "repo_analysis_summary.txt"
LOCKED_DIRS = {".core", "infra/secure", "src/engine", "internal"}

def run_analysis(payload):
    lines = []
    lines.append(f"📦 Repository Analysis Report — {datetime.now()}")
    lines.append("=" * 80)

    for root, dirs, files in os.walk("."):
        if any(root.startswith(f"./{lock}") for lock in LOCKED_DIRS):
            continue
        lines.append(f"\n📁 {root}")
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                lines.append(f"  └── {file}")
                with open(path, "r", encoding="utf-8") as f:
                    head = f.readline().strip()
                    if head.startswith("# @lock"):
                        lines.append(f"     🔒 LOCKED")
                    if "run_module" in f.read():
                        lines.append(f"     ✅ Interface: run_module() detected")

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return {"status": "ok", "summary_file": REPORT_PATH}
