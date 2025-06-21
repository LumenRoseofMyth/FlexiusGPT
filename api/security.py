from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY = os.environ.get("FLEXIUSGPT_API_KEY")
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
    return api_key
