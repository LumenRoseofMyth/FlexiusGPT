from core.router.validator import validate_payload
import os, json

def run_audit_and_upgrade_map():
    result = {"modules": [], "missing_files": [], "deprecated": [], "upgrade_recommendations": []}
    expected_dirs = ["core", "modules", "adapters", "configs"]
    expected_files = ["CORE_RULES.txt", "PHASE_MANAGER.txt", "SESSION_ENGINE.txt", "SAFETY_OVERRIDES.txt", "COMPLIANCE_ENGINE.txt", "USER_PROFILE.txt"]
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for d in expected_dirs:
        if not os.path.exists(os.path.join(base_path, d)):
            result["missing_files"].append(f"Missing directory: {d}")

    for f in expected_files:
        found = any(f in files for _, _, files in os.walk(base_path))
        if not found:
            result["missing_files"].append(f"Missing file: {f}")

    deprecated_flags = ["v1", "legacy", "old", "deprecated"]
    for root, _, files in os.walk(base_path):
        for file in files:
            if any(flag in file.lower() for flag in deprecated_flags):
                result["deprecated"].append(os.path.join(root, file))

    if result["missing_files"]:
        result["upgrade_recommendations"].append("Complete foundational logic file restoration.")
    if result["deprecated"]:
        result["upgrade_recommendations"].append("Migrate from legacy modules to latest HIMKS schema (v2.5+).")

    return json.dumps(result, indent=2)

if __name__ == "__main__":
    print(run_audit_and_upgrade_map())

@validate_payload
def run_module(*, action: str, test_mode: bool=False) -> dict:
    if action == "test_mode":
        return {"success": True, "msg": "OK"}
    return {"success": False, "msg": "unknown action"}
