import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def path_traversal_open(filename: str):
    ruta = "uploads/" + filename
    with open(ruta, "r") as archivo:
        return archivo.read()
