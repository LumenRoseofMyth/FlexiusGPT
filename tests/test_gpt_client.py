import pytest

from self_evolving_gpt.gpt_client import GPTClient


def test_generate_raises():
    client = GPTClient()
    with pytest.raises(NotImplementedError):
        client.generate("hello")

