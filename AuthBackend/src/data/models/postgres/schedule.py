from sqlalchemy import Column, DateTime, Date, Float, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Schedule(Base, TimestampMixin):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))

    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    journey_date = Column(Date)

    price = Column(Float)
    available_seats = Column(Integer)

    status = Column(String, default="active")

    bus = relationship("Bus", back_populates="schedules")
    route = relationship("Route", back_populates="schedules")
    bookings = relationship("Booking", back_populates="schedule")
