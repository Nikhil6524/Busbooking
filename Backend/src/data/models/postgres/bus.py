import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Bus(Base,TimestampMixin):
    __tablename__ = "buses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    bus_name = Column(String, nullable=False)
    bus_number = Column(String, unique=True, nullable=False)
    bus_type = Column(String)
    total_seats = Column(Integer, nullable=False)
    operator_name = Column(String)
    amenities = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    schedules = relationship("Schedule", back_populates="bus")