import os
import json
import subprocess
from datetime import datetime

MODULES_TO_CALL = [
    "env_discovery_upgrade_outline/run_audit_and_upgrade_map"
]

def scan_repository(base_path="."):
    findings = {"files": [], "python_scripts": [], "notes": []}
    for root, dirs, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            findings["files"].append(full_path)
            if file.endswith(".py"):
                findings["python_scripts"].append(full_path)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "TODO" in content or "# FIXME" in content:
                        findings["notes"].append({"file": full_path, "flag": "TODO or FIXME present"})
    return findings

def call_internal_modules():
    results = []
    for route in MODULES_TO_CALL:
        module, action = route.split("/")
        try:
            result = subprocess.run(["python3", f"modules/{module}/{action}.py"], capture_output=True, text=True)
            results.append({"module": module, "output": result.stdout.strip()})
        except Exception as e:
            results.append({"module": module, "error": str(e)})
    return results

def generate_report():
    scan = scan_repository()
    calls = call_internal_modules()
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "scan": scan,
        "module_results": calls,
        "recommendations": []
    }

    # Simple rule-based upgrade tip logic
    if len(scan["notes"]) > 0:
        report["recommendations"].append("Resolve all TODO/FIXME in Python scripts.")
    if any("deprecated" in mod.get("output", "") for mod in calls):
        report["recommendations"].append("Migrate legacy modules to HIMKS schema v2.9+.")
    return report

def repo_orchestrator():
    return generate_report()

if __name__ == "__main__":
    output = generate_report()
    print(json.dumps(output, indent=2))
