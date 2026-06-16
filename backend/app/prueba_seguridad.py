import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def sqli_plus_operator(db_conn, input_usuario: str):
    cursor = db_conn.cursor()
    query = "SELECT * FROM reservas WHERE id_evento = " + input_usuario
    cursor.execute(query)
    return cursor.fetchall()