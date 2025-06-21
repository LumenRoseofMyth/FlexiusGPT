import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def export_pr_chart(metrics: list[dict], path: str) -> str:
    """Export bar chart of PR counts to the given path."""
    dates = [m["date"] for m in metrics]
    prs = [m.get("metrics", {}).get("pull_requests", 0) for m in metrics]

    plt.figure(figsize=(6, 4))
    plt.bar(dates, prs)
    plt.xlabel("Date")
    plt.ylabel("PRs")
    plt.title("Daily PR Count")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
