from pathlib import Path
from typing import Dict

from self_evolving_gpt.repo_manager import RepoManager
from self_evolving_gpt.change_applier import ChangeApplier
from self_evolving_gpt.agents import (
    PlannerAgent,
    FileMutationAgent,
    PatchSummarizationAgent,
    PRAuthorAgent,
)
from self_evolving_gpt.prompt_builder import PromptBuilder
from self_evolving_gpt.codex_client import CodexClient
from self_evolving_gpt.testing.test_runner import TestRunner


class EvolutionOrchestrator:
    """Coordinates planning, mutation, summarization and testing."""

    def __init__(self, repo_root: str = "."):
        self.repo = RepoManager(repo_root)
        self.applier = ChangeApplier(self.repo)

        codex = CodexClient()  # stubbed client
        self.builder = PromptBuilder()

        self.planner = PlannerAgent(codex, self.builder)
        self.mutator = FileMutationAgent(codex)
        self.summarizer = PatchSummarizationAgent(self.builder, codex)
        self.pr_author = PRAuthorAgent(self.builder, codex)

        self.test_runner = TestRunner(repo_root)

    # ----- public API -----
    def evolve(self, user_goal: str, target_file: str) -> Dict[str, str]:
        """Run full evolution cycle and return results."""
        # 1) Plan
        plan = self.planner.run(user_goal, f"Repo scope: {target_file}")

        # 2) Mutate
        new_code = self.mutator.mutate_file(target_file, plan)
        self.applier.apply_full(target_file, new_code)

        # 3) Summarize diff
        diff = self._git_diff(target_file)
        summary = self.summarizer.summarize_patch(target_file, diff)

        # 4) PR metadata
        pr_meta = self.pr_author.generate_pr_metadata([summary])

        # 5) Run tests
        passed = self.test_runner.run()

        return {
            "summary": summary,
            "pr_title": pr_meta["title"],
            "pr_body": pr_meta["description"],
            "tests_passed": passed,
        }

    # ----- helpers -----
    def _git_diff(self, rel_path: str) -> str:
        """Compute a unified diff for a single file."""
        old = self.repo.read(rel_path).splitlines(keepends=True)
        new = Path(self.repo.root / rel_path).read_text().splitlines(keepends=True)
        import difflib

        return "".join(
            difflib.unified_diff(old, new, fromfile=f"a/{rel_path}", tofile=f"b/{rel_path}")
        )
