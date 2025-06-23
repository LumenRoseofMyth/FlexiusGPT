from pydantic import BaseModel, ValidationError
from datetime import datetime
import os

class Input(BaseModel):
    action: str
    data: dict

def run_module(*, payload: dict) -> dict:
    Input(**payload)

    # Ensure folder exists
    summary_dir = os.path.join(os.path.dirname(__file__), "summaries")
    os.makedirs(summary_dir, exist_ok=True)

    # Extract data
    action = payload["action"]
    data = payload["data"]
    text = data.get("text", "").strip()

    if not text:
        return {"status": "error", "message": "Missing summary text in payload"}

    # Generate filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{action}.txt"
    filepath = os.path.join(summary_dir, filename)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    return {"status": "success", "result": {"file": filename}}
