from fastapi import APIRouter
from app.api.endpoints import eventos, reservas

api_router = APIRouter()
api_router.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])
api_router.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
