import os
import requests
import base64

# GitHub repo info
GITHUB_OWNER = "LumenRoseofMyth"
GITHUB_REPO = "FlexiusGPT"
GITHUB_BRANCH = "main"

# Get your token from env var
GITHUB_TOKEN = os.environ.get("FLEXIUSGPT_GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("Please set FLEXIUSGPT_GITHUB_TOKEN environment variable.")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def debug_local_state():
    print("Current working directory:", os.getcwd())
    print("Contents of modules folder:", os.listdir("modules"))
    mb = "modules/09_knowledge_base"
    if os.path.isdir(mb):
        print(f"Contents of {mb}:", os.listdir(mb))
    else:
        print(f"Directory not found: {mb}")

def get_file_sha(path):
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}?ref={GITHUB_BRANCH}"
    print(f"GET {url} -> Status ", end="")
    response = requests.get(url, headers=headers)
    print(response.status_code)
    try:
        resp_json = response.json()
        print("Response:", resp_json if response.status_code == 200 else "")
    except Exception:
        print("Non-JSON response:", response.text)
        resp_json = None

    if response.status_code == 200 and resp_json:
        return resp_json['sha']
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"Failed to get file SHA: {response.status_code} {response.text}")

def update_github_file(path, content, commit_message):
    sha = get_file_sha(path)
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    encoded_content = base64.b64encode(content.encode()).decode()
    data = {
        "message": commit_message,
        "content": encoded_content,
        "branch": GITHUB_BRANCH
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Success: File '{path}' updated.")
        return response.json()
    else:
        raise Exception(f"Error updating file: {response.status_code} {response.text}")

if __name__ == "__main__":
    debug_local_state()
    file_path = "modules/09_knowledge_base/schema.md"
    new_content = """--- ..."""
    commit_message = "Update knowledge_base schema with refined description"
    update_github_file(file_path, new_content, commit_message)
