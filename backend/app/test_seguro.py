# Código totalmente seguro para pruebas del pipeline
def saludar_usuario(nombre: str) -> str:
    # Saludo simple y limpio
    return f"Hola, {nombre}! Bienvenido al sistema LiveSeat."

def calcular_descuento(precio: float, porcentaje: float) -> float:
    # Lógica matemática pura y segura
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("El porcentaje debe estar entre 0 y 100")
    descuento = precio * (porcentaje / 100)
    return precio - descuento
