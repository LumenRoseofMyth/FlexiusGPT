from modules.core.ingestion.github_client import GitHubAPI, fetch_repo_summary

class DummyResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data
    def raise_for_status(self):
        pass

def test_fetch_prs(monkeypatch):
    api = GitHubAPI()
    def mock_get(url, params=None):
        if 'pulls' in url:
            return DummyResponse([{"title": "PR1", "additions": 10, "deletions": 1}])
        return DummyResponse([{"title": "Issue1", "state": "open"}])
    monkeypatch.setattr(api.session, "get", mock_get)
    prs = api.fetch_prs('owner/repo')
    assert prs[0]["lines_added"] == 10
    monkeypatch.setattr('modules.core.ingestion.github_client.GitHubAPI.fetch_prs', lambda *a, **kw: [{"title": "PR1", "lines_added": 5, "lines_deleted": 1}])
    monkeypatch.setattr('modules.core.ingestion.github_client.GitHubAPI.fetch_issues', lambda *a, **kw: [{"title": "Issue1", "state": "open"}])
    summary = fetch_repo_summary('owner/repo')
    assert len(summary["prs"]) == 1
    assert len(summary["issues"]) == 1
