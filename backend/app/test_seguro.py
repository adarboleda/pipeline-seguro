# -*- coding: utf-8 -*-
"""
Archivo de prueba para validación de pipeline de seguridad.
Contiene únicamente funciones seguras y código de negocio estándar
para verificar que el analizador aprueba el archivo con éxito (Exit 0).
"""

import os
import re
import json
import hashlib
import subprocess

# ==============================================================================
# 1. LÓGICA DE NEGOCIO ESTÁNDAR
# ==============================================================================

def calcular_total_carrito(items, descuento_porcentaje=0):
    """
    Calcula el total de un carrito de compras aplicando un descuento opcional.
    """
    if not isinstance(items, list):
        raise TypeError("Los items deben ser una lista.")
        
    subtotal = 0.0
    for item in items:
        precio = item.get("precio", 0.0)
        cantidad = item.get("cantidad", 0)
        subtotal += precio * cantidad
        
    descuento = subtotal * (descuento_porcentaje / 100.0)
    total = subtotal - descuento
    return max(total, 0.0)


# ==============================================================================
# 2. VALIDACIÓN SEGURA DE ENTRADAS
# ==============================================================================

def validar_email_usuario(email):
    """
    Valida si un string tiene un formato de correo electrónico válido.
    """
    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not isinstance(email, str):
        return False
    return bool(re.match(patron_email, email))


# ==============================================================================
# 3. SUBPROCESS SEGURO — shell=False (por defecto)
# ==============================================================================

def ejecutar_ping_seguro(ip):
    """
    subprocess.run con shell=False no permite inyección de comandos.
    Los argumentos se pasan como lista sin intervención del shell del SO.
    """
    resultado = subprocess.run(["ping", "-c", "1", ip], shell=False, capture_output=True, text=True)
    return resultado.stdout


# ==============================================================================
# 4. JSON SEGURO — json.load/loads no ejecuta código arbitrario
# ==============================================================================

def cargar_configuracion(ruta_estatica):
    """
    json.load lee un archivo de configuración. JSON es un formato de datos
    puramente declarativo — no ejecuta constructores de objetos Python.
    """
    with open(ruta_estatica, "r", encoding="utf-8") as f:
        return json.load(f)


def parsear_respuesta_api(json_texto):
    """
    json.loads parsea texto JSON. Es seguro ya que JSON no permite RCE.
    """
    return json.loads(json_texto)


# ==============================================================================
# 5. CRIPTOGRAFÍA SEGURA
# ==============================================================================

def generar_hash_seguro(datos_entrada):
    """
    Genera un hash SHA-256 seguro para verificación de integridad de datos.
    """
    if not isinstance(datos_entrada, str):
        raise ValueError("La entrada debe ser una cadena de texto.")
        
    encoder = hashlib.sha256()
    encoder.update(datos_entrada.encode("utf-8"))
    return encoder.hexdigest()


# ==============================================================================
# 6. MANEJO SEGURO DE RUTAS CON VALIDACIÓN
# ==============================================================================

def leer_archivo_seguro(nombre_archivo):
    """
    Valida que la ruta final permanezca dentro del directorio base.
    Previene Path Traversal normalizando con os.path.basename.
    """
    directorio_base = os.path.abspath("uploads")
    archivo_seguro = os.path.basename(nombre_archivo)
    ruta_completa = os.path.abspath(os.path.join(directorio_base, archivo_seguro))
    
    if not ruta_completa.startswith(directorio_base):
        raise PermissionError("Acceso no autorizado fuera del directorio permitido.")
        
    with open(ruta_completa, "r") as f:
        return f.read()


# ==============================================================================
# 7. FORMATEO SEGURO DE STRINGS
# ==============================================================================

def formatear_perfil_usuario(nombre, edad):
    """
    Crea una representación limpia del perfil del usuario.
    """
    nombre_limpio = str(nombre).strip()
    edad_limpia = int(edad)
    
    return {
        "mensaje": f"Perfil de {nombre_limpio} cargado correctamente.",
        "edad": edad_limpia,
        "estado": "Activo"
    }
