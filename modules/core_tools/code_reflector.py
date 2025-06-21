import os


def summarize_codex_diff(codex_path):
    with open(codex_path, 'r') as f:
        lines = f.readlines()
    summary = []
    for line in lines:
        if 'UPGRADE_ID:' in line or '##' in line or 'feedback.append' in line or 'protocol.append' in line:
            summary.append(line.strip())
    return summary[-20:]
