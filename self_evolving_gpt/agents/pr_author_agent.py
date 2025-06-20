class PRAuthorAgent:
    def __init__(self, prompt_builder, codex_client):
        """Initialize with a PromptBuilder and Codex client."""
        self.prompt_builder = prompt_builder
        self.codex = codex_client

    def generate_pr_metadata(self, summary_list: list[str]) -> dict:
        """Generate PR title and description from diff summaries."""
        prompt = self.prompt_builder.build_pr_author_prompt(summary_list)
        response = self.codex.run(prompt)
        return self.parse_metadata(response)

    def parse_metadata(self, response: str) -> dict:
        """Parse Codex response for title and description."""
        lines = response.strip().split("\n", 1)
        return {
            "title": lines[0].replace("Title: ", "").strip(),
            "description": lines[1].replace("Description:", "").strip() if len(lines) > 1 else "",
        }
