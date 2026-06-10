from pydantic import BaseModel, Field
from typing import List

class EventoDomain(BaseModel):
    """
    Modelo de dominio interno para Evento. 
    Usado internamente y en la BD en memoria.
    """
    id: int
    nombre: str
    asientos_disponibles: int

class ReservaDomain(BaseModel):
    """
    Modelo de dominio interno para Reserva.
    """
    id: int
    evento_id: int
    email_usuario: str
    cantidad_asientos: int
    metodo_pago: str
