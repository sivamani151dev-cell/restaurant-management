from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class ReservationStatus(enum.Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    guests_count = Column(Integer, nullable=False)
    reservation_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.confirmed)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    table_id = Column(Integer, ForeignKey("tables.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))