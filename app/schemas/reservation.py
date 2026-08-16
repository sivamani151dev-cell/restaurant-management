from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.reservation import ReservationStatus

class ReservationCreate(BaseModel):
    customer_name: str
    customer_phone: str
    guests_count: int
    reservation_date: datetime
    table_id: int

class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatus] = None

class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    guests_count: int
    reservation_date: datetime
    status: ReservationStatus
    created_at: datetime
    table_id: int

    class Config:
        from_attributes = True