from self_evolving_gpt.agents import AgentBase


class AgentRunner:
    """Runs any agent with task and context inputs."""

    def __init__(self, agent: AgentBase):
        self.agent = agent

    def execute(self, task: str, context: str) -> str:
        """Execute the wrapped agent and return its output."""
        return self.agent.run(task, context)
