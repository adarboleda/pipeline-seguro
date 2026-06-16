import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def deserializacion_insegura_pickle(data_serializada):
    return pickle.loads(data_serializada)