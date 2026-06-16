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

