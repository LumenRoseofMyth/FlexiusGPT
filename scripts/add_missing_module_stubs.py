"""
Scan modules/*/schema.md and ensure each has a corresponding .py file
with a run_module() stub. Create any missing files automatically.
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

for schema in ROOT.glob("modules/*/schema.md"):
    module_dir = schema.parent
    module_py = module_dir / f"{module_dir.name}.py"
    if not module_py.exists():
        print(f"Creating missing: {module_py}")
        module_py.write_text(
            "def run_module():\n    pass\n"
        )
print("All missing module stubs created (if any).")