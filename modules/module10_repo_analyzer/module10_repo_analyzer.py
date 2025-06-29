import os
from datetime import datetime
from typing import Dict, List

REPORT_PATH = "repo_analysis_summary.txt"
LOCKED_DIRS: set[str] = {".core", "infra/secure", "src/engine", "internal"}


def run_module(payload: Dict[str, str]) -> Dict[str, str]:
    """
    Analyse repository files and write a human-readable summary.
    """
    lines: List[str] = []
    lines.append(f"📦 Repository Analysis Report — {datetime.now()}")
    lines.append("=" * 80)

    for root, _dirs, files in os.walk("."):
        if any(root.startswith(f"./{lock}") for lock in LOCKED_DIRS):
            continue
        lines.append(f"\n📁 {root}")
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                lines.append(f"  └── {file}")
                with open(path, "r", encoding="utf-8") as fp:
                    head = fp.readline().strip()
                    if head.startswith("# @lock"):
                        lines.append("     🔒 LOCKED")
                    if "run_module" in fp.read():
                        lines.append("     ✅ Interface: run_module() detected")

    with open(REPORT_PATH, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))

    return {"status": "ok", "summary_file": REPORT_PATH}
