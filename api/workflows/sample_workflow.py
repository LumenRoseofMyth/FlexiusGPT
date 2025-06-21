def run(user_log=None):
    return {
        "status": "ok",
        "message": "Sample workflow executed successfully.",
        "user_log": user_log or {}
    }
