class CodexClient:
    """Minimal interface for sending prompts to Codex models."""

    def __init__(self, model: str | None = None):
        self.model = model or "gpt-4o"

    def complete(self, prompt, **kwargs):
        raise NotImplementedError("Use Codex manually to respond to this prompt.")
