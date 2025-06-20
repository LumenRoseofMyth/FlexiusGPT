from self_evolving_gpt.runner import AgentRunner
from self_evolving_gpt.agents import AgentBase


class DummyAgent(AgentBase):
    def run(self, task, context):
        return f"{task}:{context}"

    def needs(self):
        return ["task", "context"]


def test_agent_runner_executes_all():
    runner = AgentRunner([DummyAgent()])
    result = runner.run_all("summarize diff", "diff content here")
    assert "DummyAgent" in result
    assert result["DummyAgent"] == "summarize diff:diff content here"
