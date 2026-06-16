import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def vulnerable_exec_rce(script_usuario: str):
    """
    RCE por ejecución dinámica de sentencias.
    """
    exec(script_usuario)