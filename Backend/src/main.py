from src.api.rest.app import app


@app.get("/")
async def root():
    return {
        "message": "Bus Ticket Booking Management System API Running"
    }