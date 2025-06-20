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
