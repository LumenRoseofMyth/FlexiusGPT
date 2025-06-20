from abc import ABC, abstractmethod

class AgentBase(ABC):
    """
    Abstract base class for all agents.
    Ensures consistency in how agents are executed and integrated.
    """

    @abstractmethod
    def run(self, task: str, context: str) -> str:
        """
        Run the agent with a specific task and context.
        Returns the agent's output.
        """
        pass

    @abstractmethod
    def needs(self) -> list[str]:
        """
        Declare what kind of input this agent requires (e.g., 'diff', 'file', 'code', 'prompt')
        Used by the runner to match inputs.
        """
        pass
