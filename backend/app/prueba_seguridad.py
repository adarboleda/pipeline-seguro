import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def vulnerable_subprocess_popen(cmd_argument: str):
    """
    Command Injection usando subprocess.Popen con shell=True.
    """
    subprocess.Popen(cmd_argument, shell=True)