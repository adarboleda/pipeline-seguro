from typing import List
from app.db.repository import db_repo
from app.models.domain import EventoDomain
from app.schemas.event import EventoCreate, EventoResponse

class EventService:
    @staticmethod
    def get_all_events() -> List[EventoResponse]:
        eventos = db_repo.get_all_eventos()
        return [EventoResponse(**evento.dict()) for evento in eventos]

    @staticmethod
    def create_event(data: EventoCreate) -> EventoResponse:
        # Sanitización ya ocurrió en el schema
        nuevo_evento = db_repo.create_evento(nombre=data.nombre, asientos=data.asientos_disponibles)
        return EventoResponse(**nuevo_evento.dict())
