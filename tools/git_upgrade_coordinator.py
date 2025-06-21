import subprocess
import sys

BRANCH_PREFIX = 'upgrade/deep_dive_v'


def coordinate(version: str = '1') -> None:
    branch = f"{BRANCH_PREFIX}{version}"
    subprocess.run(['git', 'checkout', '-b', branch], check=True)
    subprocess.run(['git', 'add', 'tasks/upgrade_blueprint.md', 'orchestrator_summary.md'], check=True)
    subprocess.run(['git', 'commit', '-m', 'chore(upgrade): add deep scan upgrade plan and summary'], check=True)


if __name__ == '__main__':
    ver = sys.argv[1] if len(sys.argv) > 1 else '1'
    coordinate(ver)
