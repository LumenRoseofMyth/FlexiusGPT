from self_evolving_gpt.tools.tool_registry import ToolRegistry

def test_echo_tool_registration_and_call():
    @ToolRegistry.register("echo")
    def echo_tool(x):
        return x

    tool = ToolRegistry.get("echo")
    assert tool("hello") == "hello"

def test_tool_registry_list():
    tools = ToolRegistry.list()
    assert "echo" in tools
