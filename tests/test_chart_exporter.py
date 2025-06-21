from modules.core.export.chart_exporter import export_pr_chart

def test_export_pr_chart(tmp_path):
    metrics = [{"type": "coding", "date": "2025-06-01", "metrics": {"pull_requests": 3}}]
    path = tmp_path / "chart.png"
    export_pr_chart(metrics, str(path))
    assert path.exists()
