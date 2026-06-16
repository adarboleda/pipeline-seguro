import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def vulnerable_os_system(cmd_usuario: str):
    """
    Command Injection usando os.system con concatenación directa de strings.
    """
    os.system("ping -c 4 " + cmd_usuario)