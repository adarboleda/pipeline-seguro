from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ReservaCreate(BaseModel):
    evento_id: int = Field(..., gt=0, description="El ID del evento debe ser mayor a 0.")
    email_usuario: EmailStr = Field(..., description="Correo electrónico válido del usuario.")
    cantidad_asientos: int = Field(..., gt=0, le=10, description="La cantidad de asientos por reserva debe ser entre 1 y 10.")
    metodo_pago: str = Field(..., pattern=r"^(tarjeta|paypal)$", description="El método de pago debe ser 'tarjeta' o 'paypal'.")

class ReservaResponse(BaseModel):
    id: int
    evento_id: int
    email_usuario: str
    cantidad_asientos: int
    metodo_pago: str

class ReservaConfirmacion(BaseModel):
    mensaje: str
    detalles: dict
