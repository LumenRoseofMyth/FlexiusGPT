import json
import sys
from self_evolving_gpt.api.action_server import app
from fastapi.openapi.utils import get_openapi

if __name__ == "__main__":
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    json.dump(schema, sys.stdout, indent=2)
