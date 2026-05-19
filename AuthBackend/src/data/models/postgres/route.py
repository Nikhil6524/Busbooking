from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Route(Base, TimestampMixin):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    distance = Column(Float)
    duration = Column(String)

    schedules = relationship("Schedule", back_populates="route")
