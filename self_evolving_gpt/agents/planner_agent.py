from self_evolving_gpt.agents import AgentBase
from self_evolving_gpt.prompt_builder import PromptBuilder
from self_evolving_gpt.codex_client import CodexClient


class PlannerAgent(AgentBase):
    """Plans sub-tasks based on the overall user goal. Returns step-by-step tasks."""

    def __init__(self, codex: CodexClient, builder: PromptBuilder | None = None):
        self.codex = codex
        self.builder = builder or PromptBuilder()

    def run(self, task: str, context: str) -> str:
        prompt = self.builder.build_planner_prompt(task, context)
        return self.codex.complete(prompt)

    def needs(self) -> list[str]:
        return ["task", "context"]
