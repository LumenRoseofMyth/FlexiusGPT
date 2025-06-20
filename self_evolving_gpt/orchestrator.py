"""
Module: ExecutionOrchestrator
Purpose: Orchestrates prompt construction, Codex invocation, and result handling for evolution tasks.
"""

from self_evolving_gpt.prompt_builder import PromptBuilder
from self_evolving_gpt.agents.patch_summarization_agent import PatchSummarizationAgent
from self_evolving_gpt.agents.pr_author_agent import PRAuthorAgent


class ExecutionOrchestrator:
    """Central coordinator for Codex-powered code evolution operations."""

    def __init__(self, codex_client):
        self.prompt_builder = PromptBuilder()
        self.patch_agent = PatchSummarizationAgent(self.prompt_builder, codex_client)
        self.pr_agent = PRAuthorAgent(self.prompt_builder, codex_client)

    def summarize_patch(self, patch_text: str, filename: str | None = None) -> str:
        """Return a Codex summary for the given diff."""
        return self.patch_agent.summarize_patch(filename or "", patch_text)

    def generate_pr_description(self, diff_text: str, filename: str | None = None) -> tuple[str, str]:
        """Generate a PR title and description from a diff."""
        summary = self.summarize_patch(diff_text, filename)
        metadata = self.pr_agent.generate_pr_metadata([summary])
        return metadata["title"], metadata["description"]

    def auto_evolve_from_diff(self, diff: str, filename: str | None = None) -> dict:
        """Return patch summary and PR metadata for a diff."""
        summary = self.summarize_patch(diff, filename)
        metadata = self.pr_agent.generate_pr_metadata([summary])
        return {
            "summary": summary,
            "pr_title": metadata["title"],
            "pr_body": metadata["description"],
        }
