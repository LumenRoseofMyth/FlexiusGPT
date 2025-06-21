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

load_dotenv()

# === API KEY SETUP ===
API_KEY = os.environ.get("FLEXIUSGPT_API_KEY")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

# === PATHS FOR MODULES ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from adapters.gpt_adapter import call_module_logic, run_workflow

# === FASTAPI APP ===
app = FastAPI(
    title="FlexiusGPT Analytic API",
    description="Internal API for HIMKS module analytics and workflows.",
    version="1.0.0"
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
            log_entry = f"{datetime.datetime.now()} | {endpoint} | {data} | {status}\n"
            f.write(log_entry)
    except Exception as log_err:
        print(f"Failed to log API call: {log_err}")

# === REQUEST MODELS ===
class ModuleRequest(BaseModel):
    module_id: str
    action: str
    user_log: Optional[Dict] = None

class WorkflowRequest(BaseModel):
    workflow: str
    user_log: Optional[Dict] = None

# === ENDPOINTS ===
@app.post("/module")
def api_call_module(
    req: ModuleRequest,
    api_key: APIKey = Depends(get_api_key)
):
    try:
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            call_module_logic(req.module_id, req.action, req.user_log)
        output = buf.getvalue()
        log_api_call("/module", req.dict(), "OK")
        return {"result": output}
    except Exception as e:
        log_api_call("/module", req.dict(), f"ERR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow")
def api_run_workflow(
    req: WorkflowRequest,
    api_key: APIKey = Depends(get_api_key)
):
    try:
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_workflow(req.workflow, req.user_log)
        output = buf.getvalue()
        log_api_call("/workflow", req.dict(), "OK")
        return {"result": output}
    except Exception as e:
        log_api_call("/workflow", req.dict(), f"ERR: {str(e)}")
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
    openapi_schema["servers"] = [
        {
            "url": "https://718d-130-105-158-110.ngrok-free.app",
            "description": "Ngrok tunnel for Custom GPT"
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi