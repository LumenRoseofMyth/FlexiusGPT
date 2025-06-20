from self_evolving_gpt.api import action_server
from fastapi.testclient import TestClient


class StubOrchestrator:
    def evolve(self, goal: str, filename: str):
        return {
            "summary": "stub",
            "pr_title": "title",
            "pr_body": "body",
            "tests_passed": True,
        }


def test_mutate_route(monkeypatch):
    monkeypatch.setattr(action_server, "orch", StubOrchestrator())
    client = TestClient(action_server.app)
    rsp = client.post("/mutate-file", json={"goal": "noop", "filename": "dummy.py"})
    assert rsp.status_code == 200
    assert rsp.json()["tests_passed"] is True
