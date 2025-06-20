"""
A minimal FastAPI server exposing FlexiusGPT repository functions for Custom-GPT actions.
Run via:  uvicorn self_evolving_gpt.api.action_server:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel

from self_evolving_gpt.evolution_orchestrator import EvolutionOrchestrator

app = FastAPI(
    title="FlexiusGPT Action API",
    version="0.1.0",
    description="Endpoints called by the FlexiusGPT custom action."
)

orch = EvolutionOrchestrator(".")


class MutateRequest(BaseModel):
    goal: str
    filename: str


class MutateResponse(BaseModel):
    pr_title: str
    pr_body: str
    summary: str
    tests_passed: bool


@app.post("/mutate-file", response_model=MutateResponse)
def mutate_file(req: MutateRequest):
    """Run evolution cycle on a single file and return PR metadata."""
    result = orch.evolve(req.goal, req.filename)
    return MutateResponse(**result)
