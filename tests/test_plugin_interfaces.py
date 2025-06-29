import os


def test_all_modules_have_interface_and_run_module():
    base = "modules"
    missing = []

    for module_name in os.listdir(base):
        path = os.path.join(base, module_name)
        if not os.path.isdir(path) or module_name.startswith("."):
            continue

        iface = os.path.join(path, "interface.py")
        if not os.path.isfile(iface):
            missing.append(f"{module_name}: interface.py missing")
            continue

        with open(iface, "r", encoding="utf-8") as f:
            content = f.read()
            if "def run_module" not in content:
                missing.append(f"{module_name}: run_module() missing")

    assert not missing, f"Issues in modules: {missing}"
