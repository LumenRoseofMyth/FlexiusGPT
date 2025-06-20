from self_evolving_gpt.runner import AgentRunner


class DummyAgent:
    def run(self, task, context):
        return f"ran: {task} / {context}"


def test_agent_runner():
    runner = AgentRunner(DummyAgent())
    output = runner.execute("Task", "Repo Context")
    assert output.startswith("ran:")
