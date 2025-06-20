from self_evolving_gpt.agents import PatchSummarizationAgent


class MockPromptBuilder:
    def build_diff_summary_prompt(self, diff, filename=""):
        return [
            {
                "role": "user",
                "content": f"Diff for {filename}: {diff}",
            }
        ]


class StubCodexClient:
    def run(self, prompt):
        return "Not implemented"


def test_patch_summary():
    agent = PatchSummarizationAgent(MockPromptBuilder(), StubCodexClient())
    result = agent.summarize_patch(
        "file.py", "@@ -1,2 +1,2 @@\n-print('A')\n+print('B')"
    )
    assert "Not implemented" in result
