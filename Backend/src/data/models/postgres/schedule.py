import uuid

from sqlalchemy import Column, DateTime, Date, Float, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Schedule(Base,TimestampMixin):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id"))
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id"))

    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    journey_date = Column(Date)

    price = Column(Float)
    available_seats = Column(Integer)

    status = Column(String, default="active")

    bus = relationship("Bus", back_populates="schedules")
    route = relationship("Route", back_populates="schedules")
    bookings = relationship("Booking", back_populates="schedule")