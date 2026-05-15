import uuid

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Route(Base,TimestampMixin):
    __tablename__ = "routes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id"))
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    distance = Column(Float)
    duration = Column(String)

    schedules = relationship("Schedule", back_populates="route")