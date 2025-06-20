"""
Module: FileMutationAgent
Purpose: Applies Codex-driven mutations to local source files based on structured user tasks.
"""

from self_evolving_gpt.prompt_builder import PromptBuilder


class FileMutationAgent:
    def __init__(self, codex_client):
        self.codex = codex_client
        self.builder = PromptBuilder()

    def mutate_file(self, filename: str, task: str) -> str:
        with open(filename, "r", encoding="utf-8") as f:
            context = f.read()

        prompt = self.builder.build_code_prompt(task, context)
        result = self.codex.send(prompt)

        return result.strip()  # Codex should return the full mutated file string
