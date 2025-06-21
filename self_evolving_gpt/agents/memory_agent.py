from self_evolving_gpt.agents import AgentBase
from self_evolving_gpt.memory.vector_store import VectorStore
from self_evolving_gpt.memory.memory_store import MemoryStore


class MemoryAgent(AgentBase):
    """Saves <task \u2194 answer> pairs and retrieves relevant memory for new tasks."""

    def __init__(self, store: VectorStore | None = None, memory_store: MemoryStore | None = None):
        self.store = store or VectorStore()
        self.memory_store = memory_store
        self._rating_weight = 0.0
        self._rating_count = 0

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

    def record(self, prompt: str, response: str, rating: int | None = None) -> None:
        """Persist a conversation turn and update rating weight."""
        if self.memory_store:
            self.memory_store.add_session(prompt, response, prompt, rating)
        if rating is not None:
            self._rating_weight = (
                self._rating_weight * self._rating_count + rating
            ) / (self._rating_count + 1)
            self._rating_count += 1

    @property
    def score_weight(self) -> float:
        return self._rating_weight or 1.0

    def needs(self):
        return ["task"]

