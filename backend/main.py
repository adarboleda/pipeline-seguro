from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict

app = FastAPI(
    title="LiveSeat API",
    description="API Segura para sistema de reservas de eventos LiveSeat.",
    version="1.0.0"
)

# === MODELOS DE DATOS Y VALIDACIÓN (DEFENSA EN PROFUNDIDAD) ===
# El uso estricto de Pydantic mitiga A03:2021-Injection y A04:2021-Insecure Design (OWASP Top 10).
# Al definir tipos exactos, longitudes máximas y expresiones regulares (regex),
# prevenimos que inputs maliciosos (como XSS, SQLi, o payloads masivos) lleguen a la lógica de negocio.

class Evento(BaseModel):
    id: int = Field(..., gt=0, description="El ID del evento debe ser un número entero positivo.")
    nombre: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        pattern=r"^[a-zA-Z0-9\s\-_]+$", 
        description="El nombre del evento solo puede contener caracteres alfanuméricos, espacios, guiones y guiones bajos."
    )
    asientos_disponibles: int = Field(..., ge=0, description="Los asientos disponibles no pueden ser negativos.")

class Reserva(BaseModel):
    evento_id: int = Field(..., gt=0, description="El ID del evento debe ser mayor a 0.")
    # EmailStr valida rigurosamente el formato del correo, previniendo inyecciones de strings extraños o formatos inválidos
    email_usuario: EmailStr = Field(..., description="Correo electrónico válido del usuario.")
    # Limitamos la cantidad de asientos para prevenir abusos lógicos (Denial of Wallet / Inventory Exhaustion)
    cantidad_asientos: int = Field(..., gt=0, le=10, description="La cantidad de asientos por reserva debe ser entre 1 y 10.")
    # Validamos con regex que el método de pago sea exactamente uno de los esperados
    metodo_pago: str = Field(..., pattern=r"^(tarjeta|paypal)$", description="El método de pago debe ser 'tarjeta' o 'paypal'.")


# === BASE DE DATOS SIMULADA (EN MEMORIA) ===
eventos_db: Dict[int, Evento] = {
    1: Evento(id=1, nombre="Concierto Rock Clasico", asientos_disponibles=100),
    2: Evento(id=2, nombre="Obra de Teatro LiveSeat", asientos_disponibles=50)
}


# === ENDPOINTS (RUTAS SEGURAS) ===

@app.get("/eventos", response_model=List[Evento], status_code=status.HTTP_200_OK)
async def listar_eventos():
    """
    Retorna la lista de eventos disponibles.
    No requiere input de parámetros de los usuarios (Query o Path variables), 
    minimizando drásticamente la superficie de ataque para este endpoint.
    """
    return list(eventos_db.values())


@app.post("/reservas", status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: Reserva):
    """
    Crea una reserva para un evento.
    Seguridad: El framework FastAPI junto con Pydantic rechaza automáticamente (con un HTTP 422 Unprocessable Entity) 
    cualquier payload que no cumpla estrictamente con el modelo 'Reserva' definido arriba ANTES de ejecutar este bloque.
    """
    evento = eventos_db.get(reserva.evento_id)
    if not evento:
        # Prevención de Fuga de Información (Information Leakage): 
        # Devolvemos un mensaje estándar de 404, sin revelar detalles de cómo opera nuestra DB internamente.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    
    if evento.asientos_disponibles < reserva.cantidad_asientos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay suficientes asientos disponibles para procesar su solicitud")
    
    # Lógica de negocio 
    evento.asientos_disponibles -= reserva.cantidad_asientos
    
    return {
        "mensaje": "Reserva confirmada exitosamente",
        "detalles": {
            "evento_id": reserva.evento_id,
            "asientos_reservados": reserva.cantidad_asientos
        }
    }
