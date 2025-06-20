import tempfile
from self_evolving_gpt.agents.file_mutation import FileMutationAgent


class StubCodex:
    def send(self, prompt):
        return "# Updated file content\nprint('Mutated')"


def test_mutate_file_logic():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write("print('Original')\n")
        temp_file.flush()

        agent = FileMutationAgent(StubCodex())
        result = agent.mutate_file(temp_file.name, "Change print message")

        assert "Mutated" in result
