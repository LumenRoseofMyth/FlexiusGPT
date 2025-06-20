from self_evolving_gpt.memory.vector_store import VectorStore


def test_vector_store_retrieval():
    store = VectorStore()
    store.add("implement vector memory")
    store.add("refactor compliance engine")
    result = store.query("memory implementation", top_k=1)
    assert "vector memory" in result[0]
