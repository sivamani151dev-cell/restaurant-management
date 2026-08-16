from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.menu_item import MenuItem, FoodCategory
from app.models.user import User
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/menu", tags=["Menu"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=MenuItemResponse, status_code=201)
def create_menu_item(item: MenuItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category,
        is_vegetarian=item.is_vegetarian
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[MenuItemResponse])
def get_menu(category: Optional[FoodCategory] = None, vegetarian_only: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(MenuItem).filter(MenuItem.is_available == True)
    if category:
        query = query.filter(MenuItem.category == category)
    if vegetarian_only:
        query = query.filter(MenuItem.is_vegetarian == True)
    return query.all()

@router.put("/{item_id}", response_model=MenuItemResponse)
def update_menu_item(item_id: int, update: MenuItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    if update.name is not None:
        item.name = update.name
    if update.price is not None:
        item.price = update.price
    if update.is_available is not None:
        item.is_available = update.is_available
    if update.is_vegetarian is not None:
        item.is_vegetarian = update.is_vegetarian
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=204)
def delete_menu_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return None