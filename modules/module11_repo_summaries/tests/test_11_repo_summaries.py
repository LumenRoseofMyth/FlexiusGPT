from modules.module11_repo_summaries.interface import run_module

def test_run_module_summary_saves():
    payload = {
        "action": "save_summary",
        "data": {
            "text": "This is a test summary."
        }
    }
    result = run_module(payload=payload)
    assert result["status"] == "success"
