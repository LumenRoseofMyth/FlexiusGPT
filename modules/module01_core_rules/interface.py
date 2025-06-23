from pydantic import BaseModel
import os


class Input(BaseModel):
    action: str
    data: dict


def run_module(*, payload: dict) -> dict:
    Input(**payload)  # validation check

    issues = {
        "missing_interface": [],
        "missing_run_module": [],
        "missing_init": [],
        "missing_lock": [],
    }

    # Check for required files and structure
    for module in os.listdir("modules"):
        if module.startswith("."):
            continue

        path = os.path.join("modules", module)
        iface = os.path.join(path, "interface.py")
        init_file = os.path.join(path, "__init__.py")

        if not os.path.exists(path):
            continue
        if not os.path.isfile(iface):
            issues["missing_interface"].append(module)
            continue
        if not os.path.isfile(init_file):
            issues["missing_init"].append(module)
        else:
            with open(iface, encoding="utf-8") as f:
                if "def run_module" not in f.read():
                    issues["missing_run_module"].append(module)

    # Check @lock headers
    for zone in [".core", "infra/secure"]:
        for root, _, files in os.walk(zone):
            for f in files:
                if f.startswith(".") or f.endswith(".gitkeep"):
                    continue
                full_path = os.path.join(root, f)
                with open(full_path, encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    if first_line != "# @lock":
                        issues["missing_lock"].append(full_path)

    return {"status": "checked", "issues": issues}
