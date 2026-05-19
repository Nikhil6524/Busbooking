from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel


class BusCreate(BaseModel):
    owner_id: Optional[str] = None
    bus_name: str
    bus_number: str
    bus_type: Optional[str] = None
    total_seats: int
    operator_name: Optional[str] = None
    amenities: Optional[str] = None


class BusUpdate(BaseModel):
    owner_id: Optional[str] = None
    bus_name: Optional[str] = None
    bus_number: Optional[str] = None
    bus_type: Optional[str] = None
    total_seats: Optional[int] = None
    operator_name: Optional[str] = None
    amenities: Optional[str] = None


class RouteCreate(BaseModel):
    bus_id: int
    source: str
    destination: str
    distance: Optional[float] = None
    duration: Optional[str] = None


class RouteUpdate(BaseModel):
    bus_id: Optional[int] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    distance: Optional[float] = None
    duration: Optional[str] = None


class ScheduleCreate(BaseModel):
    bus_id: int
    route_id: int
    departure_time: datetime
    arrival_time: datetime
    journey_date: date
    price: float
    available_seats: int
    status: Optional[str] = "active"


class ScheduleUpdate(BaseModel):
    bus_id: Optional[int] = None
    route_id: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    journey_date: Optional[date] = None
    price: Optional[float] = None
    available_seats: Optional[int] = None
    status: Optional[str] = None


class AdminAddRequest(BaseModel):
    entity: Literal["bus", "route", "schedule"]
    data: BusCreate | RouteCreate | ScheduleCreate


class AdminUpdateRequest(BaseModel):
    entity: Literal["bus", "route", "schedule"]
    id: int
    data: BusUpdate | RouteUpdate | ScheduleUpdate


class AdminDeleteRequest(BaseModel):
    entity: Literal["bus", "route", "schedule"]
    id: int
