from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    table_id: int
    items: list[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price: float
    menu_item_id: int

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    table_id: int
    items: list[OrderItemResponse] = []

    class Config:
        from_attributes = True
