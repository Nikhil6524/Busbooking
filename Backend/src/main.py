from fastapi import FastAPI

app = FastAPI(title="Bus Ticket Booking Management System")


@app.get("/")
async def root():
    return {
        "message": "Bus Ticket Booking Management System API Running"
    }