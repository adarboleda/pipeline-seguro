import re
from typing import List, Optional
import hashlib

def validar_caracteres_entrada(entrada: str) -> bool:
    """
    Validación de seguridad: Solo permite caracteres alfanuméricos
    y restringe la longitud a un rango seguro.
    """
    if not entrada or len(entrada) > 30:
        return False
    patron = r"^[a-zA-Z0-9\-_]+$"
    return bool(re.match(patron, entrada))

def formatear_mensaje_bienvenida(usuario: str) -> str:
    """
    Formateo seguro: Uso de f-strings nativos sin ejecución
    dinámica de comandos ni concatenación SQL.
    """
    if not validar_caracteres_entrada(usuario):
        raise ValueError("Entrada no válida por políticas de seguridad")
    return f"Hola, {usuario}! Tu sesión en LiveSeat ha iniciado con éxito."

def hashear_password_segura(contrasena: str, salt: bytes) -> str:
    """
    Criptografía Segura: Uso de algoritmos robustos con derivación de llaves (PBKDF2)
    en lugar de hashes simples obsoletos.
    """
    dk = hashlib.pbkdf2_hmac(
        'sha256', 
        contrasena.encode('utf-8'), 
        salt, 
        100000
    )
    return dk.hex()