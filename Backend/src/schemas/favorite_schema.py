from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    bus_id: int
