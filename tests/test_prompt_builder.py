from self_evolving_gpt.prompt_builder import PromptBuilder


def test_build_code_prompt():
    pb = PromptBuilder()
    prompt = pb.build_code_prompt("Fix foo", "def foo(): pass")

    assert isinstance(prompt, list)
    assert len(prompt) == 1
    item = prompt[0]
    assert item["role"] == "user"
    content = item["content"]
    assert "Task:" in content
    assert '"""' in content
