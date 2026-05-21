from typing import Optional

from pydantic import BaseModel


class RouteResponse(BaseModel):
    id: int
    bus_id: int
    source: str
    destination: str
    distance: Optional[float] = None
    duration: Optional[str] = None

    model_config = {"from_attributes": True}
