import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

LLAVE_API_SUPER_SECRETA = "AIzaSyD-1234567890-ABCDE-FGHIJ"

def hash_password_sha1(contrasena: str) -> str:
    hasher = hashlib.sha1()
    hasher.update(contrasena.encode('utf-8'))
    return hasher.hexdigest()

