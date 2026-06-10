from fastapi import APIRouter, status
from typing import List
from app.schemas.event import EventoCreate, EventoResponse
from app.services.event_service import EventService

router = APIRouter()

@router.get("/", response_model=List[EventoResponse], status_code=status.HTTP_200_OK)
async def listar_eventos():
    """
    Retorna la lista de eventos disponibles.
    No requiere parámetros de usuario (Query o Path variables), 
    minimizando drásticamente la superficie de ataque.
    """
    return EventService.get_all_events()

@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
async def crear_evento(evento: EventoCreate):
    """
    Crea un nuevo evento.
    El input es sanitizado estrictamente con Pydantic y Bleach en el Schema.
    """
    return EventService.create_event(evento)
