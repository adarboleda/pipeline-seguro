import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def sqli_percent_operator(db_conn, input_usuario: str):
    cursor = db_conn.cursor()
    query = "SELECT * FROM productos WHERE nombre = '%s'" % input_usuario
    cursor.execute(query)
    return cursor.fetchall()