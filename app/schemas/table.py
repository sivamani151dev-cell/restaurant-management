from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TableCreate(BaseModel):
    table_number : int
    capacity: int

class TableUpdate(BaseModel):
    is_occupied: Optional[bool] = None
    capacity: Optional[int] = None

class TableResponse(BaseModel):
    id: int
    table_number : int
    capacity: int
    is_occupied: bool
    created_at : datetime

    class Config:
        from_attributes=True