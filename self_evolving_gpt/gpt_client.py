class GPTClient:
    def __init__(self, model=None):
        self.model = model or "gpt-4o"

    def generate(self, prompt, **kwargs):
        raise NotImplementedError("Use Codex manually to respond to this prompt.")
