from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.table import Table
from app.models.user import User
from app.schemas.table import TableCreate, TableUpdate, TableResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tables", tags=["Tables"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=TableResponse, status_code=201)
def create_table(table: TableCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Table).filter(Table.table_number == table.table_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Table number already exists")
    new_table = Table(table_number=table.table_number, capacity=table.capacity)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.get("/", response_model=list[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@router.put("/{table_id}", response_model=TableResponse)
def update_table(table_id: int, update: TableUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    if update.is_occupied is not None:
        table.is_occupied = update.is_occupied
    if update.capacity is not None:
        table.capacity = update.capacity
    db.commit()
    db.refresh(table)
    return table