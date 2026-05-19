from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Route(Base,TimestampMixin):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey("buses.id", ondelete="CASCADE"))
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    distance = Column(Float)
    duration = Column(String)

    bus = relationship("Bus", back_populates="routes")
    schedules = relationship(
        "Schedule",
        back_populates="route",
        cascade="all, delete-orphan",
        passive_deletes=True
    )