import uuid
from typing import Optional

from pydantic import BaseModel


class BusResponse(BaseModel):
    id: int
    owner_id: Optional[uuid.UUID] = None
    bus_name: str
    bus_number: str
    bus_type: Optional[str] = None
    total_seats: int
    operator_name: Optional[str] = None
    amenities: Optional[str] = None

    model_config = {"from_attributes": True}
