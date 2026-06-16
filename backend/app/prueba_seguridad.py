import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

# ==============================================================================
# CATEGORÍA 1: Ejecución Remota de Código (RCE) / Inyección de Comandos
# ==============================================================================

def vulnerable_eval_rce(payload_usuario: str):
    """
    RCE por ejecución dinámica de código.
    """
    eval(payload_usuario)

def vulnerable_exec_rce(script_usuario: str):
    """
    RCE por ejecución dinámica de sentencias.
    """
    exec(script_usuario)

def vulnerable_os_system(cmd_usuario: str):
    """
    Command Injection usando os.system con concatenación directa de strings.
    """
    os.system("ping -c 4 " + cmd_usuario)

def vulnerable_subprocess_popen(cmd_argument: str):
    """
    Command Injection usando subprocess.Popen con shell=True.
    """
    subprocess.Popen(cmd_argument, shell=True)

def vulnerable_subprocess_call(cmd_argument: str):
    """
    Command Injection usando subprocess.call con shell=True.
    """
    subprocess.call("ls -la " + cmd_argument, shell=True)


# ==============================================================================
# CATEGORÍA 2: Inyección SQL (SQLi) mediante Concatenaciones Inseguras
# ==============================================================================

def sqli_format_concatenation(db_conn, input_usuario: str):
    """
    SQL Injection mediante concatenación usando .format()
    """
    cursor = db_conn.cursor()
    query = "SELECT * FROM usuarios WHERE email = '{}'".format(input_usuario)
    cursor.execute(query)
    return cursor.fetchall()

def sqli_percent_operator(db_conn, input_usuario: str):
    """
    SQL Injection mediante formateador de strings '%'
    """
    cursor = db_conn.cursor()
    query = "SELECT * FROM productos WHERE nombre = '%s'" % input_usuario
    cursor.execute(query)
    return cursor.fetchall()

def sqli_plus_operator(db_conn, input_usuario: str):
    """
    SQL Injection mediante concatenación aritmética '+'
    """
    cursor = db_conn.cursor()
    query = "SELECT * FROM reservas WHERE id_evento = " + input_usuario
    cursor.execute(query)
    return cursor.fetchall()

def sqli_fstring_operator(db_conn, input_usuario: str):
    """
    SQL Injection mediante f-strings con palabras clave de base de datos
    """
    cursor = db_conn.cursor()
    query = f"SELECT * FROM auditorias WHERE descripcion = {input_usuario}"
    cursor.execute(query)
    return cursor.fetchall()


# ==============================================================================
# CATEGORÍA 3: Deserialización Insegura (RCE / DoS)
# ==============================================================================

def deserializacion_insegura_pickle(data_serializada):
    """
    Inseguridad crítica: deserializar datos arbitrarios de usuario usando pickle.
    """
    return pickle.loads(data_serializada)

def deserializacion_insegura_yaml(data_yaml_usuario):
    """
    Inseguridad en YAML: Carga insegura sin SafeLoader.
    """
    return yaml.load(data_yaml_usuario)


# ==============================================================================
# CATEGORÍA 4: Path Traversal (Lectura y Escritura de Archivos Arbitrarios)
# ==============================================================================

def path_traversal_open(filename: str):
    """
    Permite lectura arbitraria de archivos del sistema al concatenar '../'
    """
    ruta = "uploads/" + filename
    with open(ruta, "r") as archivo:
        return archivo.read()


# ==============================================================================
# CATEGORÍA 5: Criptografía Débil y Hardcoding de Secretos
# ==============================================================================

# Secreto hardcodeado en el código fuente (Fuga de credenciales)
LLAVE_API_SUPER_SECRETA = "AIzaSyD-1234567890-ABCDE-FGHIJ"

def hash_password_md5(contrasena: str) -> str:
    """
    Uso de MD5, un algoritmo criptográfico obsoleto y vulnerable a colisiones.
    """
    hasher = hashlib.md5()
    hasher.update(contrasena.encode('utf-8'))
    return hasher.hexdigest()

def hash_password_sha1(contrasena: str) -> str:
    """
    Uso de SHA1, algoritmo desaconsejado para hashing de contraseñas.
    """
    hasher = hashlib.sha1()
    hasher.update(contrasena.encode('utf-8'))
    return hasher.hexdigest()


# ==============================================================================
# CATEGORÍA 6: Cross-Site Scripting (XSS) y SSRF
# ==============================================================================

def xss_manually_formatted_html(nombre_usuario: str) -> str:
    """
    Generación manual de plantillas HTML concatenando variables directamente.
    """
    return "<html><body><h1>Bienvenido " + nombre_usuario + "</h1></body></html>"

def ssrf_untrusted_request(url_usuario: str):
    """
    SSRF: Peticiones HTTP a URLs provistas por el usuario sin sanitizar.
    """
    return requests.get(url_usuario)