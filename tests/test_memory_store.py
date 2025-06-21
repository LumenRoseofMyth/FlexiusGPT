from self_evolving_gpt.memory.memory_store import MemoryStore


def test_memory_store_add_search(tmp_path):
    path = tmp_path / "mem.jsonl"
    store = MemoryStore(path)
    store.add_session("hello", "world", "hello world", rating=4)
    store.add_session("foo", "bar", "foo bar", rating=2)
    results = store.search("hello")
    assert len(results) == 1
    assert results[0]["prompt"] == "hello"
    assert store.average_rating() == 3.0
