from typing import List, Dict, Optional
from app.models.domain import EventoDomain, ReservaDomain

# Simulación de la base de datos en memoria
class Repository:
    def __init__(self):
        self.eventos_db: Dict[int, EventoDomain] = {
            1: EventoDomain(id=1, nombre="Concierto Rock Clasico", asientos_disponibles=100),
            2: EventoDomain(id=2, nombre="Obra de Teatro LiveSeat", asientos_disponibles=50)
        }
        self.reservas_db: Dict[int, ReservaDomain] = {}
        self._next_reserva_id = 1
        self._next_evento_id = 3

    def get_all_eventos(self) -> List[EventoDomain]:
        return list(self.eventos_db.values())

    def get_evento_by_id(self, evento_id: int) -> Optional[EventoDomain]:
        return self.eventos_db.get(evento_id)

    def create_evento(self, nombre: str, asientos: int) -> EventoDomain:
        evento = EventoDomain(
            id=self._next_evento_id,
            nombre=nombre,
            asientos_disponibles=asientos
        )
        self.eventos_db[self._next_evento_id] = evento
        self._next_evento_id += 1
        return evento

    def update_evento(self, evento: EventoDomain) -> None:
        self.eventos_db[evento.id] = evento

    def create_reserva(self, evento_id: int, email: str, cantidad: int, metodo_pago: str) -> ReservaDomain:
        reserva = ReservaDomain(
            id=self._next_reserva_id,
            evento_id=evento_id,
            email_usuario=email,
            cantidad_asientos=cantidad,
            metodo_pago=metodo_pago
        )
        self.reservas_db[self._next_reserva_id] = reserva
        self._next_reserva_id += 1
        return reserva

    def get_all_reservas(self) -> List[ReservaDomain]:
        return list(self.reservas_db.values())

# Instancia global del repositorio (Singleton simulado)
db_repo = Repository()
