import os
import json

def run_audit_and_upgrade_map():
    result = {
        "modules": [],
        "missing_files": [],
        "deprecated": [],
        "upgrade_recommendations": []
    }

    # Define expected directories and key HIMKS logic files
    expected_dirs = [
        "core", "modules", "adapters", "configs"
    ]
    expected_files = [
        "CORE_RULES.txt", "PHASE_MANAGER.txt", "SESSION_ENGINE.txt",
        "SAFETY_OVERRIDES.txt", "COMPLIANCE_ENGINE.txt", "USER_PROFILE.txt"
    ]

    # Check for expected directories and files
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    for d in expected_dirs:
        dir_path = os.path.join(base_path, d)
        if not os.path.exists(dir_path):
            result["missing_files"].append(f"Missing directory: {d}")

    for f in expected_files:
        found = False
        for root, _, files in os.walk(base_path):
            if f in files:
                found = True
                break
        if not found:
            result["missing_files"].append(f"Missing file: {f}")

    # Detect deprecated placeholder
    deprecated_flags = ["v1", "legacy", "old", "deprecated"]
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(flag in file.lower() for flag in deprecated_flags):
                result["deprecated"].append(os.path.join(root, file))

    # Recommend upgrades based on observed state
    if result["missing_files"]:
        result["upgrade_recommendations"].append("Complete foundational logic file restoration.")
    if result["deprecated"]:
        result["upgrade_recommendations"].append("Migrate from legacy modules to latest HIMKS schema (v2.5+).")

    return json.dumps(result, indent=2)

# If this script is run directly
if __name__ == "__main__":
    print(run_audit_and_upgrade_map())
