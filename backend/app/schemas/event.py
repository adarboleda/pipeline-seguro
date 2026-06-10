from pydantic import BaseModel, Field, validator
import bleach

class EventoCreate(BaseModel):
    nombre: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        pattern=r"^[a-zA-Z0-9\s\-_]+$", 
        description="Nombre del evento (caracteres alfanuméricos permitidos)."
    )
    asientos_disponibles: int = Field(..., ge=0, description="Los asientos disponibles no pueden ser negativos.")

    @validator("nombre")
    def sanitize_nombre(cls, value: str) -> str:
        # Sanitización estricta contra XSS eliminando cualquier tag HTML potencial
        sanitized = bleach.clean(value, tags=[], attributes={}, strip=True)
        return sanitized

class EventoResponse(BaseModel):
    id: int
    nombre: str
    asientos_disponibles: int
