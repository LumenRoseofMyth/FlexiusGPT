# Trigger PR diff – no functional change
class PromptBuilder:
    def __init__(self):
        self.system_msg = "You are a repo-aware developer assistant."

    def build_code_prompt(self, task: str, context: str) -> list[dict]:
        message = (
            f"{self.system_msg}\n\n"
            f"Task:\n{task.strip()}\n\n"
            f"Context:\n\"\"\"\n{context.strip()}\n\"\"\"\n\n"
            f"Respond with only the complete updated code block."
        )
        return [{"role": "user", "content": message}]
