from self_evolving_gpt.agents import PlannerAgent
from self_evolving_gpt.prompt_builder import PromptBuilder


class DummyCodex:
    def complete(self, prompt):
        return "\u2022 Step 1: Analyze goal\n\u2022 Step 2: Create plan"


def test_planner_agent_runs():
    agent = PlannerAgent(DummyCodex(), PromptBuilder())
    result = agent.run("Build a Codex loop", "Current repo: FlexiusGPT")
    assert "Step" in result
