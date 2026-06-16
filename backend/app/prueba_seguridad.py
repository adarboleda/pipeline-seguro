import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def sqli_format_concatenation(db_conn, input_usuario: str):
    cursor = db_conn.cursor()
    query = "SELECT * FROM usuarios WHERE email = '{}'".format(input_usuario)
    cursor.execute(query)
    return cursor.fetchall()