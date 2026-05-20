from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas.bus_schema import BusResponse
from src.schemas.route_schema import RouteResponse


class ScheduleResponse(BaseModel):
    id: int
    bus_id: int
    route_id: int
    departure_time: datetime
    arrival_time: datetime
    journey_date: date
    price: float
    available_seats: int
    status: Optional[str] = None

    model_config = {"from_attributes": True}


class SeatMapResponse(BaseModel):
    total_seats: int
    available_seats: int
    booked_seats: list[str]
    available_seat_numbers: list[str]


class CombinedScheduleSearchResponse(BaseModel):
    bus: BusResponse
    route: RouteResponse
    schedule: ScheduleResponse
