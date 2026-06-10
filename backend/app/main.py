from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="LiveSeat API",
    description="API Segura para sistema de reservas de eventos LiveSeat. (Clean Architecture)",
    version="1.1.0"
)

# Incluir las rutas de forma modular
app.include_router(api_router)
