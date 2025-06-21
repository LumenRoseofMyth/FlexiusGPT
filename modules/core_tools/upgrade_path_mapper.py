import json
import os
from typing import List

REPORT_PATH = 'orchestrator_report.json'
OUTPUT_PATH = os.path.join('tasks', 'upgrade_blueprint.md')

def gather_suggestions(report: dict) -> List[str]:
    suggestions = []
    notes = report.get('scan', {}).get('notes', [])
    for note in notes:
        file = note.get('file')
        flag = note.get('flag', 'note')
        suggestions.append(f"Address {flag} in {file}")

    for mod in report.get('module_results', []):
        if 'error' in mod:
            suggestions.append(f"Investigate failure in {mod['module']}")
        output = mod.get('output', '')
        if isinstance(output, str) and 'deprecated' in output.lower():
            suggestions.append(f"Update deprecated code in {mod['module']}")
    return suggestions

def write_blueprint(suggestions: List[str], path: str = OUTPUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('### HIMKS Upgrade Recommendations:\n')
        for s in suggestions:
            f.write(f"- [ ] {s}\n")

def build_upgrade_blueprint(report_path: str = REPORT_PATH, output_path: str = OUTPUT_PATH) -> str:
    if not os.path.exists(report_path):
        raise FileNotFoundError(report_path)
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    suggestions = gather_suggestions(report)
    write_blueprint(suggestions, output_path)
    return output_path

if __name__ == '__main__':
    path = build_upgrade_blueprint()
    print(f"Upgrade blueprint saved to {path}")
