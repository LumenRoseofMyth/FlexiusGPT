import subprocess

def run_discovery():
    subprocess.run(
        ["python", "modules/env_discovery_upgrade_outline/discovery_upgrade_outline.py"],
        check=True
    )

if __name__ == "__main__":
    run_discovery()
