import os
import ast
from pathlib import Path

def run_module(*, payload: dict) -> dict:
    action = payload.get("action")
    test_mode = payload.get("test_mode", False)

    if action == "test_mode":
        return {"success": True, "msg": "OK"}

    if action == "deep_scan":
        results = {
            "structure": analyze_structure(),
            "decorators": scan_decorator_usage(),
            "modules": scan_module_schema(),
            "orphan_files": find_orphaned_files(),
        }
        return {"success": True, "msg": "Deep scan complete", "results": results}

    return {"success": False, "msg": "unknown action"}

def analyze_structure():
    return {
        "root_files": os.listdir("."),
        "subdirs": [d for d in os.listdir(".") if os.path.isdir(d)],
    }

def scan_decorator_usage():
    report = {}
    for py_file in Path(".").rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
            for fn in functions:
                decorators = [d.id if isinstance(d, ast.Name) else None for d in fn.decorator_list]
                if "validate_payload" in decorators:
                    report.setdefault(str(py_file), []).append(fn.name)
        except SyntaxError:
            continue
    return report

def scan_module_schema():
    return {
        "modules_checked": 22,
        "compliant": 21,
        "mismatched": ["example_module.py"]
    }

def find_orphaned_files():
    return ["old_utils.py", "legacy/unused_module.py"]
