"""
ARCHIVO EDUCATIVO - VULNERABILIDADES INTENCIONALES
Propósito: Demostrar vulnerabilidades comunes en aplicaciones Python/FastAPI.
NO usar en producción.
"""

import sqlite3
import subprocess
import pickle
import os
import hashlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="App Vulnerable - Solo educativo")

# ------------------------------------------------------------------ #
# VULN-1: SQL Injection                                               #
# ------------------------------------------------------------------ #
@app.get("/users")
def get_user(username: str):
    conn = sqlite3.connect("liveseat.db")
    cursor = conn.cursor()
    # VULNERABLE: concatenación directa de entrada del usuario en SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return {"results": rows}


# ------------------------------------------------------------------ #
# VULN-2: Command Injection                                           #
# ------------------------------------------------------------------ #
@app.get("/ping")
def ping_host(host: str):
    # VULNERABLE: shell=True con entrada del usuario permite inyección
    result = subprocess.run(
        f"ping -n 1 {host}",
        shell=True,
        capture_output=True,
        text=True
    )
    return {"output": result.stdout}


# ------------------------------------------------------------------ #
# VULN-3: Deserialización insegura (Insecure Deserialization)        #
# ------------------------------------------------------------------ #
@app.post("/load-session")
async def load_session(request: Request):
    body = await request.body()
    # VULNERABLE: pickle.loads sobre datos no confiables permite RCE
    session_data = pickle.loads(body)
    return {"session": str(session_data)}


# ------------------------------------------------------------------ #
# VULN-4: Path Traversal                                              #
# ------------------------------------------------------------------ #
@app.get("/files")
def read_file(filename: str):
    # VULNERABLE: sin validación permite leer archivos arbitrarios del SO
    base_path = "C:/ESPE/Seguro/pipeline-seguro/backend/uploads/"
    with open(base_path + filename, "r") as f:
        content = f.read()
    return {"content": content}


# ------------------------------------------------------------------ #
# VULN-5: XSS (Cross-Site Scripting) reflejado                       #
# ------------------------------------------------------------------ #
@app.get("/search", response_class=HTMLResponse)
def search(q: str):
    # VULNERABLE: devuelve la entrada del usuario sin escapar en HTML
    html = f"""
    <html>
      <body>
        <h2>Resultados para: {q}</h2>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


# ------------------------------------------------------------------ #
# VULN-6: Contraseñas con hash débil (MD5 sin salt)                  #
# ------------------------------------------------------------------ #
def hash_password_insecure(password: str) -> str:
    # VULNERABLE: MD5 es rápido y sin salt → vulnerable a rainbow tables
    return hashlib.md5(password.encode()).hexdigest()


@app.post("/register")
def register(username: str, password: str):
    hashed = hash_password_insecure(password)
    conn = sqlite3.connect("liveseat.db")
    conn.execute(
        f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed}')"
    )
    conn.commit()
    conn.close()
    return {"message": "Usuario registrado"}


# ------------------------------------------------------------------ #
# VULN-7: Exposición de variables de entorno sensibles               #
# ------------------------------------------------------------------ #
@app.get("/debug/env")
def debug_env():
    # VULNERABLE: expone todas las variables de entorno (tokens, secrets, etc.)
    return {"env": dict(os.environ)}


# ------------------------------------------------------------------ #
# VULN-8: IDOR (Insecure Direct Object Reference)                    #
# ------------------------------------------------------------------ #
@app.get("/reservations/{reservation_id}")
def get_reservation(reservation_id: int):
    # VULNERABLE: no verifica que el usuario autenticado sea el dueño
    conn = sqlite3.connect("liveseat.db")
    row = conn.execute(
        f"SELECT * FROM reservations WHERE id = {reservation_id}"
    ).fetchone()
    conn.close()
    return {"reservation": row}
