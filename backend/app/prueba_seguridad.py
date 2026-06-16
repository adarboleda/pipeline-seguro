import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def ssrf_untrusted_request(url_usuario: str):

    return requests.get(url_usuario)