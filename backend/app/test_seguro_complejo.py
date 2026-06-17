# -*- coding: utf-8 -*-
"""
Archivo de prueba seguro adicional (Complejo)
Contiene patrones avanzados de código seguro para verificar que el modelo no genere falsos positivos.
"""

import os
import sys
import yaml
import json
import hashlib
import requests
import subprocess
from pathlib import Path
from urllib.parse import urlparse

# 1. Base de datos con SQLAlchemy (Parametrizada / ORM)
class DatabaseHandler:
    def __init__(self, session):
        self.session = session

    def query_user_profile(self, user_id: int):
        # Seguro: consulta de SQLAlchemy con filtrado seguro
        return self.session.query(User).filter(User.id == user_id).first()

    def update_status_safe(self, email: str, new_status: str):
        # Seguro: consulta parametrizada
        query = "UPDATE users SET status = :status WHERE email = :email"
        self.session.execute(query, {"status": new_status, "email": email})

# 2. Deserialización segura
def load_app_config(config_yaml_str: str):
    # Seguro: yaml.safe_load o Loader=yaml.SafeLoader
    return yaml.safe_load(config_yaml_str)

def parse_server_response(json_payload: str):
    # Seguro: json.loads no ejecuta código Python arbitrario
    return json.loads(json_payload)

# 3. Subprocess seguro sin shell
def count_lines_in_file(filepath: str):
    # Seguro: shell=False, lista de argumentos, no inyección de comandos
    if not os.path.exists(filepath):
        return 0
    res = subprocess.run(["wc", "-l", filepath], capture_output=True, text=True, shell=False)
    return res.stdout.strip()

# 4. Manejo de archivos seguro contra Path Traversal
def serve_user_avatar(avatar_filename: str):
    base_directory = Path("/var/www/uploads").resolve()
    # Seguro: sanitización estricta del nombre del archivo y verificación de prefijo
    safe_filename = Path(avatar_filename).name
    target_path = (base_directory / safe_filename).resolve()
    
    if not str(target_path).startswith(str(base_directory)):
        raise PermissionError("Intento de path traversal detectado.")
        
    if target_path.exists():
        return target_path.read_bytes()
    return b""

# 5. Criptografía robusta
def compute_secure_checksum(data: bytes):
    # Seguro: sha256 no es una función de hash rota (como md5 o sha1)
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()

# 6. SSRF mitigado (validación de host)
ALLOWED_API_DOMAINS = {"api.github.com", "api.stripe.com"}

def call_external_api(url: str):
    parsed_url = urlparse(url)
    if parsed_url.netloc not in ALLOWED_API_DOMAINS:
        raise ValueError("Acceso denegado a host no autorizado.")
    
    # Seguro: el host está validado antes de realizar la petición HTTP
    response = requests.get(url, timeout=10)
    return response.json()
