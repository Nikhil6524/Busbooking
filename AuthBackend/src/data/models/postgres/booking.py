import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Booking(Base, TimestampMixin):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"))

    seat_number = Column(String, nullable=False)
    booking_status = Column(String, default="confirmed")
    booking_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    schedule = relationship("Schedule", back_populates="bookings")
