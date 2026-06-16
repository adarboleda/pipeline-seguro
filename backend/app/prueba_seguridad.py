import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def deserializacion_insegura_yaml(data_yaml_usuario):
    return yaml.load(data_yaml_usuario)