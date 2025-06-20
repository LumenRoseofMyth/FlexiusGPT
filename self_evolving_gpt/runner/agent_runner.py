# self_evolving_gpt/runner/agent_runner.py

from self_evolving_gpt.agents import AgentBase

class AgentRunner:
    """Discovers and executes agents that implement the AgentBase interface."""

    def __init__(self, agents: list[AgentBase]):
        self.agents = agents

    def run_all(self, task: str, context: str) -> dict:
        """Runs all agents with the provided task/context and collects their outputs."""
        results = {}
        for agent in self.agents:
            agent_name = agent.__class__.__name__
            if not isinstance(agent, AgentBase):
                raise TypeError(f"{agent_name} does not implement AgentBase.")
            try:
                output = agent.run(task, context)
                results[agent_name] = output
            except Exception as e:
                results[agent_name] = f"Error: {str(e)}"
        return results
