from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine, Base
from app.routers import auth, menu, tables, reservations, orders
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Management System",
    description="A complete restaurant management backend API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(tables.router)
app.include_router(orders.router)
app.include_router(reservations.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")