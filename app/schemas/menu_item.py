from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.menu_item import FoodCategory

class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: FoodCategory
    is_vegetarian: bool = False

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    is_vegetarian: Optional[bool] = None

class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: FoodCategory
    is_available: bool
    is_vegetarian: bool
    created_at : datetime

    class Config:
        from_attributes = True