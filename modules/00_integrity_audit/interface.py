from typing import Dict
import os


def run_module(payload: Dict) -> Dict:
    """
    Governance audit module.
    Checks structure and policy adherence.
    """
    results = {
        "missing_locks": [],
        "invalid_plugins": [],
        "invalid_interfaces": [],
    }

    # 1. Check for @lock in protected areas
    for base in [".core", "infra/secure"]:
        for root, _, files in os.walk(base):
            for f in files:
                if f.startswith(".") or f.endswith(".gitkeep"):
                    continue
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    first = file.readline().strip()
                    if first != "# @lock":
                        results["missing_locks"].append(
                            path
                        )

    # 2. Check plugin folders
    for mod in os.listdir("modules"):
        mod_path = os.path.join("modules", mod)
        if (
            not os.path.isdir(mod_path)
            or mod.startswith(".")
            or not mod[0].isdigit()
        ):
            continue

        iface = os.path.join(mod_path, "interface.py")
        if not os.path.isfile(iface):
            results["invalid_plugins"].append(mod)
            continue

        with open(iface, "r", encoding="utf-8") as f:
            if "def run_module" not in f.read():
                results["invalid_interfaces"].append(mod)

    return {
        "status": "fail" if any(results.values()) else "pass",
        "results": results
    }
