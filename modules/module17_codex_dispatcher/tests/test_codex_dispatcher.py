import sys
import importlib

sys.path.insert(0, ".")


def test_dispatcher_meta_report():
    mod = importlib.import_module(
        "modules.module17_codex_dispatcher.interface"
    )
    result = mod.run_module(
        payload={"action": "meta_report", "data": {}}
    )
    assert result["status"] == "ok"
    assert result["source"] == "meta_report"
    assert "result" in result


def test_dispatcher_invalid_action():
    mod = importlib.import_module(
        "modules.module17_codex_dispatcher.interface"
    )
    result = mod.run_module(
        payload={"action": "invalid", "data": {}}
    )
    assert result["status"] == "error"
    assert "Unknown action" in result["message"]
