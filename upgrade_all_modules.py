# upgrade_all_modules.py
import os
from datetime import datetime

MODULE_DIR = "modules"
LOG_FILE = "codex_upgrade_log.txt"
EXCLUDE_FILES = {"__init__.py", "schema.md", "schema.bak", "README.md"}

def list_module_files():
    files = []
    for root, dirs, filenames in os.walk(MODULE_DIR):
        for f in filenames:
            if f.endswith(".py") and f not in EXCLUDE_FILES:
                files.append(os.path.join(root, f))
    return files

def mark_file_for_codex(path):
    marker = f"# Codex Upgrade Timestamp: {datetime.utcnow().isoformat()}Z\n"
    with open(path, "r", encoding="utf-8") as file:
        content = file.readlines()

    if any("Codex Upgrade Timestamp" in line for line in content):
        return  # Already marked

    with open(path, "w", encoding="utf-8") as file:
        file.write(marker)
        file.writelines(content)

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.utcnow()}] Marked: {path}\n")

if __name__ == "__main__":
    print("Scanning module logic files...")
    files = list_module_files()
    for f in files:
        mark_file_for_codex(f)
    print(f"Marked {len(files)} module files for Codex upgrade.")
