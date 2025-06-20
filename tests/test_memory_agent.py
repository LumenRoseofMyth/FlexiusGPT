from self_evolving_gpt.agents.memory_agent import MemoryAgent


def test_memory_agent_add_and_query():
    agent = MemoryAgent()
    out1 = agent.run("build vector store", "")
    assert "No prior" in out1
    agent.run("vector store retrieval", "")
    out2 = agent.run("vector store retrieval", "")
    assert "vector store" in out2
