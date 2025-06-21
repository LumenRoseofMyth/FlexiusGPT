from self_evolving_gpt.agents import AgentBase
from self_evolving_gpt.memory.vector_store import VectorStore


class MemoryAgent(AgentBase):
    """Saves <task \u2194 answer> pairs and retrieves relevant memory for new tasks."""

    def __init__(self, store: VectorStore | None = None):
        self.store = store or VectorStore()

    # AgentBase ------------
    def run(self, task: str, context: str) -> str:
        # retrieve memories to help current agent chain
        memories = self.store.query(task, 3)
        joined = "\n---\n".join(memories) if memories else "No prior memory."

        if context:
            commit_refs = self.store.query(context, 1)
            if commit_refs:
                joined += f"\nCommitRef: {commit_refs[0]}"
            self.store.add(context)

        # Save this task for future
        self.store.add(task)
        return joined

    def needs(self):
        return ["task"]

