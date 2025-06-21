import argparse
import json

from modules.core.twin.digital_twin_engine import DigitalTwin


def forecast(twin_state: dict) -> str:
    meta = twin_state.get("meta", {})
    volatility = meta.get("commit_volatility", 0)
    circadian = meta.get("circadian_rhythm_hour", None)
    lines = []
    if volatility < 1:
        lines.append("### Momentum: expect steady progress next week.")
    else:
        lines.append("### Volatility high: commit activity may fluctuate.")
    if circadian is not None:
        lines.append(f"Average commit hour: {circadian:.1f}h")
    return "\n".join(lines)


def main(state_file: str, out_file: str):
    with open(state_file) as f:
        state = json.load(f)
    report = forecast(state)
    with open(out_file, "w") as f:
        f.write(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("state_file")
    parser.add_argument("out_file", nargs="?", default="forecast.md")
    args = parser.parse_args()
    main(args.state_file, args.out_file)

