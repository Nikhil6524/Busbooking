from pydantic import BaseModel, constr


class BookingCreate(BaseModel):
    schedule_id: int
    seat_number: constr(pattern=r"^\d{1,3}[A-Za-z]{1}$")
