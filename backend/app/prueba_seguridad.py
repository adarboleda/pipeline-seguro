import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests


# Secreto hardcodeado en el código fuente (Fuga de credenciales)
LLAVE_API_SUPER_SECRETA = "AIzaSyD-1234567890-ABCDE-FGHIJ"

def hash_password_md5(contrasena: str) -> str:
    """
    Uso de MD5, un algoritmo criptográfico obsoleto y vulnerable a colisiones.
    """
    hasher = hashlib.md5()
    hasher.update(contrasena.encode('utf-8'))
    return hasher.hexdigest()
