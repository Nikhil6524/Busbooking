import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.models.postgres.base import Base, TimestampMixin


class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
