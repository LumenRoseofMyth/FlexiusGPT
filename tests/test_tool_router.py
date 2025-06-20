from self_evolving_gpt.agents.dispatcher_agent import DispatcherAgent
from self_evolving_gpt.tools import tool_registry  # ensures decorators run


def test_add_tool():
    agent = DispatcherAgent()
    cmd = '{"tool": "calc.add", "args": {"a": 2, "b": 3}}'
    out = agent.run(cmd, "")
    assert '"result": 5' in out
