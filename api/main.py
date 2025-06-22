import sys
import os
import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Optional, Dict
from pathlib import Path

load_dotenv()

# === API KEY SETUP ===
API_KEY = os.environ.get("FLEXIUSGPT_API_KEY")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=401, detail="Invalid or missing API Key")

# === PATHS FOR MODULES ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from adapters.gpt_adapter import call_module_logic
from modules.core.io.connector import get_active_connector_url
from workflows import WORKFLOWS

# === FASTAPI APP ===
app = FastAPI(
    title="FlexiusGPT Analytic API",
    description="Internal API for HIMKS module analytics and workflows.",
    version="1.1.0"
)

# === MOUNT .WELL-KNOWN FOR CHATGPT ACTIONS ===
well_known_path = os.path.join(os.path.dirname(__file__), ".well-known")
app.mount("/.well-known", StaticFiles(directory=well_known_path), name="plugin-meta")

# === AUDIT LOGGING ===
def log_api_call(endpoint, data, status):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = os.path.join(log_folder, f"api_access_{date_str}.log")
    try:
        with open(log_file, "a") as f:
            log_entry = (
                f"{datetime.datetime.now()} | {endpoint} | {data} | {status}\n"
            )
            f.write(log_entry)
    except Exception as log_err:
        print(f"Failed to log API call: {log_err}")

# === REQUEST MODELS ===
class ModuleRequest(BaseModel):
    module_id: str
    action: str
    user_log: Optional[Dict] = None


class FeedbackRequest(BaseModel):
    feedback_data: Dict
    user_profile: Optional[Dict] = None
    session_outcome: Optional[Dict] = None
    context: Optional[Dict] = None

# === ENDPOINTS ===

@app.get("/modules", tags=["registry"])
def list_modules():
    base = Path(__file__).parents[1] / "modules"
    mods = [p.name for p in base.iterdir() if p.is_dir()]
    return {"modules": mods}
@app.post("/module")
def api_call_module(
    req: ModuleRequest,
    api_key: APIKey = Depends(get_api_key)
):
    payload = req.dict()
    module_id = payload.pop("module_id")
    try:
        result = call_module_logic(module_id, payload)
        log_api_call("/module", req.dict(), "OK")
        return result
    except HTTPException as e:
        log_api_call("/module", req.dict(), f"ERR: {e.detail}")
        raise e
    except Exception as e:
        log_api_call("/module", req.dict(), f"ERR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow")
def api_run_workflow(
    req: Dict,
    api_key: APIKey = Depends(get_api_key)
):
    name = req.pop("workflow", None)
    if not name or name not in WORKFLOWS:
        raise HTTPException(status_code=404, detail=f"Unknown workflow: {name}")
    try:
        result = WORKFLOWS[name](payload=req)
        log_api_call("/workflow", {"workflow": name}, "OK")
        return result
    except HTTPException as e:
        log_api_call("/workflow", req, f"ERR: {e.detail}")
        raise e
    except Exception as e:
        log_api_call("/workflow", req, f"ERR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
def api_feedback(
    req: FeedbackRequest,
    api_key: APIKey = Depends(get_api_key)
):
    try:
        from modules.core.feedback.feedback_engine import process_feedback
        nudge = process_feedback(
            req.user_profile or {},
            req.feedback_data,
            req.session_outcome,
            req.context,
        )
        log_api_call("/feedback", req.dict(), "OK")
        return {"nudge": nudge}
    except Exception as e:
        log_api_call("/feedback", req.dict(), f"ERR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === OPENAPI ENDPOINT FOR CUSTOM GPTs ===

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    server_url = (
        os.environ.get("CONNECTOR_PUBLIC_URL")
        or get_active_connector_url()
        or "http://localhost:8000"
    )
    openapi_schema["servers"] = [
        {
            "url": server_url,
            "description": "Ngrok tunnel for Custom GPT",
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
