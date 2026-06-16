import os
import subprocess
import pickle
import yaml
import hashlib
import sqlite3
import requests

def vulnerable_subprocess_call(cmd_argument: str):
    """
    Command Injection usando subprocess.call con shell=True.
    """
    subprocess.call("ls -la " + cmd_argument, shell=True)