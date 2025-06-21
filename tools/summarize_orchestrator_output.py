import json

# Load the saved report
with open("orchestrator_report.json", "r") as f:
    report = json.load(f)

summary = []

# Add high-level metadata
summary.append(f"## 🧠 HIMKS Deep Scan Summary Report")
summary.append(f"**Generated:** {report.get('timestamp', 'Unknown')}")

# Recommendations
recs = report.get("recommendations", [])
if recs:
    summary.append("\n### ✅ Recommendations:")
    for rec in recs:
        summary.append(f"- {rec}")
else:
    summary.append("\n✅ No actionable recommendations at this time.")

# Flags from scan results
notes = report.get("scan", {}).get("notes", [])
if notes:
    summary.append("\n### ⚠️ Comment flags found:")
    for note in notes[:10]:  # limit to first 10
        summary.append(f"- {note['file']} ({note['flag']})")

# Output to markdown file
with open("orchestrator_summary.md", "w") as f:
    f.write("\n".join(summary))

print("Summary saved to orchestrator_summary.md")
