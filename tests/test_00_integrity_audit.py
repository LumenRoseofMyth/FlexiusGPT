import sys
import importlib


sys.path.insert(
    0,
    "."
)


def test_repo_integrity_audit():
    mod = importlib.import_module(
        "modules.00_integrity_audit.interface"
    )
    payload = {
        "payload": {
            "action":
            "scan",
            "data": {}
        }
    }
    result = mod.run_module(
        payload
    )
    assert result["status"] == "pass", (
        f"Integrity issues found: {result['details']}"
    )
