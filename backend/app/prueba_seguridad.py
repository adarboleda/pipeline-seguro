import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests


def ssrf_untrusted_request(url_usuario: str):
    """
    SSRF: Peticiones HTTP a URLs provistas por el usuario sin sanitizar.
    """
    return requests.get(url_usuario)