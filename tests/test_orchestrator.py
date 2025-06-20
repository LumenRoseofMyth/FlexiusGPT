from self_evolving_gpt.orchestrator import ExecutionOrchestrator


class StubCodex:
    def run(self, prompt):
        return "Stub Codex Response"


def test_orchestrator_flow():
    orchestrator = ExecutionOrchestrator(StubCodex())
    result = orchestrator.auto_evolve_from_diff("diff --git a/x.py b/x.py", "x.py")

    assert isinstance(result, dict)
    assert "summary" in result
    assert "pr_title" in result
    assert "pr_body" in result
