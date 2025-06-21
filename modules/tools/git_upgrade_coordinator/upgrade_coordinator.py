import subprocess
import sys

BRANCH_PREFIX = 'upgrade/deep_dive_v'


def coordinate(version: str = '1') -> None:
    branch = f"{BRANCH_PREFIX}{version}"
    subprocess.run(['git', 'checkout', '-b', branch], check=True)
    subprocess.run(['git', 'add', 'tasks/upgrade_blueprint.md', 'orchestrator_summary.md'], check=True)
    subprocess.run(['git', 'commit', '-m', 'chore(upgrade): add deep scan upgrade plan and summary'], check=True)

def create_phase_enforcement_branch():
    # Existing branch and commit logic here, but use the Phase Enforcement Blueprint
    import subprocess, shutil
    import os

    branch = "upgrade/phase_enforcement_v1"
    subprocess.run(["git", "checkout", "-b", branch], check=True)

    # Ensure the file exists and is added
    src = "tasks/phase_enforcement_blueprint.md"
    dst = "tasks/phase_enforcement_blueprint.md"
    if os.path.exists(src):
        subprocess.run(["git", "add", dst])
        subprocess.run([
            "git", "commit", "-m",
            "chore(upgrade): add phase enforcement blueprint"
        ])
    else:
        print("Phase enforcement blueprint file not found.")

    # Optionally push the branch
    subprocess.run(["git", "push", "-u", "origin", branch], check=True)

if __name__ == '__main__':
    ver = sys.argv[1] if len(sys.argv) > 1 else '1'
    coordinate(ver)
