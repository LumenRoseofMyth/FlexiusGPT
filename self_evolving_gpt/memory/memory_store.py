import json
from pathlib import Path
from typing import List, Dict, Optional
import datetime


class MemoryStore:
    """Persistent JSONL store for prompt/response sessions."""

    def __init__(self, path: str | Path = "memory.jsonl"):
        self.path = Path(path)
        if not self.path.exists():
            self.path.touch()

    def add_session(self, prompt: str, response: str, query: str, rating: Optional[int] = None) -> None:
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "query": query,
            "rating": rating,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def search(self, keyword: str) -> List[Dict]:
        """Return sessions that contain the keyword in prompt or response."""
        results: List[Dict] = []
        if not self.path.exists():
            return results
        key = keyword.lower()
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                text = f"{data.get('prompt','')} {data.get('response','')}".lower()
                if key in text:
                    results.append(data)
        return results

    def average_rating(self) -> float:
        ratings = []
        if not self.path.exists():
            return 0.0
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                if isinstance(data.get("rating"), int):
                    ratings.append(data["rating"])
        return sum(ratings) / len(ratings) if ratings else 0.0
