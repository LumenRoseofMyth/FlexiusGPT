import os
import requests
import base64
from datetime import date
from pathlib import Path
import shutil

GITHUB_OWNER = "LumenRoseofMyth"
GITHUB_REPO = "FlexiusGPT"
GITHUB_BRANCH = "main"
GITHUB_TOKEN = os.environ.get("FLEXIUSGPT_GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise Exception("Missing FLEXIUSGPT_GITHUB_TOKEN environment variable.")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_sha(path):
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}?ref={GITHUB_BRANCH}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["sha"]
    elif r.status_code == 404:
        return None
    else:
        raise Exception(f"Error getting SHA for {path}: {r.status_code} - {r.text}")

def update_schema_file(path):
    print(f"🔍 Processing {path}")
    sha = get_sha(path)
    if not sha:
        print(f"⏭️ Skipping (not found on GitHub): {path}")
        return

    # Backup original locally
    local_path = Path(path)
    backup_path = local_path.with_suffix(".bak")
    shutil.copy(local_path, backup_path)

    # Read and patch content
    with open(local_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("version:"):
            new_lines.append("version: 1.0.1\n")
        elif line.startswith("last_reviewed:"):
            new_lines.append(f"last_reviewed: {date.today()}\n")
        else:
            new_lines.append(line)

    new_content = "".join(new_lines)

    # Safety check: never push short or empty file
    if len(new_content.strip()) < 20 or "module_name:" not in new_content:
        print(f"❌ Skipping: suspicious content in {path}")
        return

    encoded = base64.b64encode(new_content.encode()).decode()
    data = {
        "message": f"chore: update schema.md (bulk review {date.today()})",
        "content": encoded,
        "sha": sha,
        "branch": GITHUB_BRANCH
    }

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    r = requests.put(url, headers=headers, json=data)
    if r.status_code in [200, 201]:
        print(f"✅ Updated: {path}")
    else:
        print(f"❌ Failed: {path} | {r.status_code} | {r.text}")

if __name__ == "__main__":
    module_dir = "modules"
    for module in sorted(os.listdir(module_dir)):
        schema_path = f"{module_dir}/{module}/schema.md"
        if os.path.exists(schema_path):
            update_schema_file(schema_path)
