from self_evolving_gpt.tools.tool_registry import ToolRegistry


@ToolRegistry.register("calc.add")
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@ToolRegistry.register("calc.mul")
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
