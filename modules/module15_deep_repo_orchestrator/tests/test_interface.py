from modules.module15_deep_repo_orchestrator import interface


def test_orchestrator_runs():
    result = interface.run_module(
        payload={"action": "test", "data": {}}
    )
    assert result["status"] == "complete"
