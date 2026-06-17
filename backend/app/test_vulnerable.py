# -*- coding: utf-8 -*-
"""
Archivo de prueba para verificar la detección de código vulnerable en el CI/CD pipeline.
Contiene deliberadamente patrones vulnerables (Categorías 2 a 6).
"""

import os
import sys
import yaml
import json
import pickle
import hashlib
import requests
import subprocess

# ==============================================================================
# CATEGORÍA 2: Inyección de Comandos / Código
# ==============================================================================

def ejecutar_comando_usuario(ip_usuario):
    """
    VULNERABLE: os.system ejecuta comandos concatenando entrada sin sanitizar.
    """
    os.system("ping -c 1 " + ip_usuario)

def evaluar_expresion_dinamica(data_usuario):
    """
    VULNERABLE: eval() permite la ejecución de código Python arbitrario.
    """
    return eval(data_usuario)


# ==============================================================================
# CATEGORÍA 3: Deserialización Insegura
# ==============================================================================

def cargar_objeto_pickle(datos_serializados):
    """
    VULNERABLE: pickle.loads deserializa objetos arbitrarios y permite RCE.
    """
    return pickle.loads(datos_serializados)

def cargar_configuracion_yaml(yaml_crudo):
    """
    VULNERABLE: yaml.load sin SafeLoader permite instanciación de objetos arbitrarios.
    """
    return yaml.load(yaml_crudo)


# ==============================================================================
# CATEGORÍA 4: Path Traversal
# ==============================================================================

def descargar_reporte_usuario(nombre_archivo):
    """
    VULNERABLE: Permite Path Traversal al concatenar directorios y nombres de archivos sin validar.
    """
    ruta_completa = "uploads/" + nombre_archivo
    with open(ruta_completa, "r") as f:
        return f.read()


# ==============================================================================
# CATEGORÍA 5: Secretos Hardcodeados y Criptografía Débil
# ==============================================================================

# VULNERABLE: Fuga de credenciales hardcodeadas
TOKEN_ACCESO_PRODUCCION = "sk-proj-1234567890ABCDEF1234567890ABCDEF"

def hash_contrasena_md5(password_plano):
    """
    VULNERABLE: MD5 está obsoleto y expuesto a colisiones rápidas.
    """
    h = hashlib.md5()
    h.update(password_plano.encode("utf-8"))
    return h.hexdigest()


# ==============================================================================
# CATEGORÍA 6: XSS y SSRF
# ==============================================================================

def respuesta_html_insegura(nombre):
    """
    VULNERABLE: Permite Cross-Site Scripting (XSS) al no escapar la entrada en HTML.
    """
    return "<html><body><h1>Hola " + nombre + "</h1></body></html>"

def consultar_api_externa(url_destino):
    """
    VULNERABLE: Server-Side Request Forgery (SSRF) al hacer peticiones a URLs arbitrarias provistas por el usuario.
    """
    return requests.get(url_destino)
