from fastapi import HTTPException, status
from app.db.repository import db_repo
from app.schemas.reservation import ReservaCreate, ReservaResponse, ReservaConfirmacion
from typing import List

class ReservationService:
    @staticmethod
    def create_reservation(data: ReservaCreate) -> ReservaConfirmacion:
        evento = db_repo.get_evento_by_id(data.evento_id)
        if not evento:
            # Prevención de Fuga de Información: HTTP 404 sin detalles internos
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
        
        if evento.asientos_disponibles < data.cantidad_asientos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No hay suficientes asientos disponibles para procesar su solicitud"
            )
        
        # Lógica de negocio (actualizar inventario)
        evento.asientos_disponibles -= data.cantidad_asientos
        db_repo.update_evento(evento)
        
        # Registrar la reserva
        reserva = db_repo.create_reserva(
            evento_id=data.evento_id,
            email=data.email_usuario,
            cantidad=data.cantidad_asientos,
            metodo_pago=data.metodo_pago
        )
        
        return ReservaConfirmacion(
            mensaje="Reserva confirmada exitosamente",
            detalles={
                "evento_id": reserva.evento_id,
                "asientos_reservados": reserva.cantidad_asientos,
                "reserva_id": reserva.id
            }
        )

    @staticmethod
    def get_all_reservations() -> List[ReservaResponse]:
        reservas = db_repo.get_all_reservas()
        return [ReservaResponse(**reserva.dict()) for reserva in reservas]
