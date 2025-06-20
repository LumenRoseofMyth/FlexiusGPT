from self_evolving_gpt.agents import PRAuthorAgent


class MockPromptBuilder:
    def build_pr_author_prompt(self, summary_list):
        return [{"role": "user", "content": "mock prompt"}]


class StubCodexClient:
    def run(self, prompt):
        return "Title: Test\n\nDescription: Testing"


def test_pr_author_agent_output_format():
    agent = PRAuthorAgent(MockPromptBuilder(), StubCodexClient())
    result = agent.generate_pr_metadata(["Updated foo.py", "Refactored bar logic"])
    assert "title" in result and "description" in result
