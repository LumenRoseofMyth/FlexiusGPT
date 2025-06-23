import sys
import importlib

sys.path.insert(0, ".")


def test_meta_reporter_creates_output_files():
    mod = importlib.import_module("modules.module16_meta_reporter.interface")
    result = mod.run_module(payload={"action": "test", "data": {}})
    assert result["status"] == "complete"
    assert "json_file" in result["output"]
    assert "txt_file" in result["output"]
