# \ud83d\udd10 Codex Block: SPEC004BATCH03CODEX_UTILITIES

Date: 2025-06-21

from datetime import datetime

CODEX_TEMPLATE = """
\n\ud83d\udd10 Codex Block: SPEC{spec_id}BATCH{batch_num}{block_name}

Date: {date}

"""


def generate_codex_boilerplate(spec_id: str, batch_num: str, block_name: str) -> str:
    """Create a standard Codex block header."""
    today = datetime.today().strftime("%Y-%m-%d")
    block_header = CODEX_TEMPLATE.format(
        spec_id=spec_id,
        batch_num=batch_num.zfill(2),
        block_name=block_name.upper(),
        date=today,
    )
    return block_header


def create_codex_file(target_path: str, spec_id: str, batch_num: str, block_name: str) -> None:
    """Write Codex boilerplate to the given file path."""
    boilerplate = generate_codex_boilerplate(spec_id, batch_num, block_name)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(boilerplate)
    print(f"\u2705 Created: {target_path}")


if __name__ == "__main__":
    validate = False
    try:
        from codex_validator import validate_codex_structure  # type: ignore
        validate = True
    except Exception:
        pass
    if validate:
        validate_codex_structure()
    # Example: create_codex_file("modules/core/protocol/new_logic.py", "004", "03", "PROTOCOL_FORECAST_CARD")
