import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def xss_manually_formatted_html(nombre_usuario: str) -> str:
    return "<html><body><h1>Bienvenido " + nombre_usuario + "</h1></body></html>"

