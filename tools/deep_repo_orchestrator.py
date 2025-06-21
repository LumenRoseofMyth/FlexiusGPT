from modules.deep_repo_orchestrator import repo_orchestrator

# Expose generate_report for backward compatibility

def generate_report():
    return repo_orchestrator.generate_report()
