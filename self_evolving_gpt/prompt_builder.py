# Trigger PR diff – PromptBuilder v4 (adds diff summary)
import json

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

    def build_planner_prompt(self, goal: str, context: str) -> list[dict]:
        prompt = (
            f"{self.system_msg}\n\n"
            f"User Goal:\n{goal.strip()}\n\n"
            f"Project Context:\n\"\"\"\n{context.strip()}\n\"\"\"\n\n"
            f"Break down the goal into a step-by-step technical plan. Use bullet points. No code yet."
        )
        return [{"role": "user", "content": prompt}]

    def build_pr_author_prompt(self, summary_list: list[str]) -> list[dict]:
        joined = "\n- ".join([""] + summary_list)
        prompt = (
            f"{self.system_msg}\n\n"
            f"Write a concise GitHub PR title and a short description based on these changes:\n"
            f"{joined}\n\n"
            f"Format:\n"
            f"Title: <title here>\n\nDescription: <description here>"
        )
        return [{"role": "user", "content": prompt}]

    def build_diff_summary_prompt(self, diff: str, filename: str = "") -> list[dict]:
        """Construct a prompt directing Codex to summarize a code diff."""

        header = f"Filename: {filename}\n\n" if filename else ""
        message = (
            f"{self.system_msg}\n\n"
            "Task:\nSummarize the functional changes in the following code diff "
            "for inclusion in a GitHub pull request description.\n\n"
            f"{header}"
            f"Diff:\n\"\"\"\n{diff.strip()}\n\"\"\"\n\n"
            "Respond with a concise summary of what was changed, focusing on "
            "functionality and structure."
        )
        return [{"role": "user", "content": message}]

    def build_memory_prompt(self, task: str, memories: str) -> list[dict]:
        prompt = (
            f"{self.system_msg}\n\n"
            f"Task:\n{task}\n\n"
            f"Previous relevant context:\n\"\"\"\n{memories}\n\"\"\"\n\n"
            f"Use these memories when answering."
        )
        return [{"role": "user", "content": prompt}]

    def build_tool_call_prompt(self, tool_name: str, **kwargs) -> list[dict]:
        payload = {"tool": tool_name, "args": kwargs}
        return [{"role": "user", "content": json.dumps(payload)}]
