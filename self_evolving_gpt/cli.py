import argparse, sys
from self_evolving_gpt.evolution_orchestrator import EvolutionOrchestrator


def main():
    ap = argparse.ArgumentParser(description="Run EvolutionOrchestrator")
    ap.add_argument("--goal", required=True, help="High-level user goal")
    ap.add_argument("--file", required=True, help="Target file to mutate")
    ap.add_argument("--repo", default=".", help="Repo root")
    args = ap.parse_args()

    orch = EvolutionOrchestrator(args.repo)
    result = orch.evolve(args.goal, args.file)
    print("=== Evolution Summary ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    sys.exit(main())
