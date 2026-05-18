from src.api.rest.auth_app import app


@app.get("/")
async def root():
    return {
        "message": "Auth service running"
    }
