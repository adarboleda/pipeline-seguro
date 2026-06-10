from fastapi import APIRouter, status
from typing import List
from app.schemas.reservation import ReservaCreate, ReservaResponse, ReservaConfirmacion
from app.services.reservation_service import ReservationService

router = APIRouter()

@router.post("/", response_model=ReservaConfirmacion, status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: ReservaCreate):
    """
    Crea una reserva para un evento.
    Seguridad: FastAPI + Pydantic rechazan automáticamente entradas inválidas o masivas.
    """
    return ReservationService.create_reservation(reserva)

@router.get("/", response_model=List[ReservaResponse], status_code=status.HTTP_200_OK)
async def listar_reservas():
    """
    Retorna la lista de todas las reservas efectuadas.
    """
    return ReservationService.get_all_reservations()
