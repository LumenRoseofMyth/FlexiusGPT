import json
import inspect
from self_evolving_gpt.agents import AgentBase
from self_evolving_gpt.tools.tool_registry import ToolRegistry


class DispatcherAgent(AgentBase):
    """
    Receives a JSON command: {"tool": "...", "args": {...}}
    Executes the tool and returns JSON {"result": ...}
    """

    def run(self, task: str, context: str) -> str:
        try:
            cmd = json.loads(task)
            tool_name = cmd["tool"]
            args = cmd.get("args", {})
            fn = ToolRegistry.get(tool_name)
            if not fn:
                return json.dumps({"error": f"Unknown tool {tool_name}"})
            bound = inspect.signature(fn).bind(**args)
            result = fn(*bound.args, **bound.kwargs)
            return json.dumps({"result": result})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def needs(self):
        return ["task"]
