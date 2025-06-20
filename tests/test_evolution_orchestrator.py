from self_evolving_gpt.evolution_orchestrator import EvolutionOrchestrator


class StubOrchestrator(EvolutionOrchestrator):
    def __init__(self, tmpdir):
        super().__init__(tmpdir)

    def evolve(self, user_goal, target_file):
        return {
            "summary": "stub summary",
            "pr_title": "stub title",
            "pr_body": "stub body",
            "tests_passed": True,
        }


def test_orchestrator_stub(tmp_path):
    orch = StubOrchestrator(tmp_path)
    result = orch.evolve("Add foo", "foo.py")
    assert result["tests_passed"] is True
