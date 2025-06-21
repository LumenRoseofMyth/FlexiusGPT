import requests

class GitHubAPI:
    """Minimal GitHub API client used for ingestion."""

    def __init__(self, token: str | None = None):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.github+json"})
        if token:
            self.session.headers["Authorization"] = f"token {token}"

    def fetch_prs(self, repo: str, state: str = "open", limit: int = 5) -> list[dict]:
        """Return list of PR summaries for a repo."""
        url = f"https://api.github.com/repos/{repo}/pulls"
        resp = self.session.get(url, params={"state": state, "per_page": limit})
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "title": pr.get("title", ""),
                "lines_added": pr.get("additions", 0),
                "lines_deleted": pr.get("deletions", 0),
            }
            for pr in data
        ]

    def fetch_issues(self, repo: str, state: str = "open", limit: int = 5) -> list[dict]:
        """Return list of issue summaries for a repo."""
        url = f"https://api.github.com/repos/{repo}/issues"
        resp = self.session.get(url, params={"state": state, "per_page": limit})
        resp.raise_for_status()
        data = resp.json()
        summaries = []
        for issue in data:
            if "pull_request" in issue:
                # skip PRs returned in issues endpoint
                continue
            summaries.append({
                "title": issue.get("title", ""),
                "state": issue.get("state", ""),
                "created_at": issue.get("created_at", ""),
            })
        return summaries


def fetch_repo_summary(repo: str, token: str | None = None, limit: int = 5) -> dict:
    """Fetch PR and issue summaries for a repository."""
    api = GitHubAPI(token)
    return {
        "prs": api.fetch_prs(repo, limit=limit),
        "issues": api.fetch_issues(repo, limit=limit),
    }
