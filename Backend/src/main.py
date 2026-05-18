from src.api.rest.business_app import app


@app.get("/")
async def root():
    return {
        "message": "Business service running"
    }