class PatchSummarizationAgent:
    def __init__(self, prompt_builder, codex_client):
        """Initialize with dependencies for prompting and Codex access."""
        self.prompt_builder = prompt_builder
        self.codex = codex_client

    def summarize_patch(self, filename: str, patch: str) -> str:
        """Generate a summary of a code patch using Codex."""
        prompt = self.prompt_builder.build_diff_summary_prompt(patch, filename)
        return self.codex.run(prompt)
