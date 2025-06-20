![CI](https://github.com/${{github.repository}}/actions/workflows/ci.yml/badge.svg)
![Self-Evolve](https://github.com/${{github.repository}}/actions/workflows/self_evolve.yml/badge.svg)
# 🔧 Project Setup

```bash
python -m venv venv
pip install -r requirements.txt
cp .env.example .env

# Then customize values as needed
```

## Usage

```python
from self_evolving_gpt.prompt_builder import PromptBuilder

builder = PromptBuilder()
prompt = builder.build_code_prompt("Add foo", "def foo(): pass")
print(prompt)
```

### Using FlexiusGPT as a Custom-GPT Action

1. Run the API locally or deploy:
   ```bash
   uvicorn self_evolving_gpt.api.action_server:app --host 0.0.0.0 --port 8000
   ```
2. Generate `openapi.json`:
   ```bash
   python scripts/export_openapi.py > openapi.json
   ```
3. In the ChatGPT builder:
   - Authentication: **None** (or "API Key" if you add header auth)
   - Paste the contents of `openapi.json` in "Schema".
   - Update → Done.
