import subprocess
import yaml
import hashlib
import urllib.request
import os

def run_user_cmd_safe(cmd: str):
    # Safe Cat 2: Executing echo safely as argument list with shell=False
    subprocess.run(["echo", cmd], shell=False)

def deserialize_payload_safe(payload: str):
    # Safe Cat 3: yaml.safe_load does not execute arbitrary code
    return yaml.safe_load(payload)

def get_user_avatar_safe(user_id: str):
    # Safe Cat 4: Using os.path.basename to clean input and a static path join
    clean_id = os.path.basename(user_id)
    path = os.path.join("static", "avatars", f"{clean_id}.png")
    # Using realpath to ensure path remains inside static/avatars directory
    abs_path = os.path.realpath(path)
    abs_base = os.path.realpath(os.path.join("static", "avatars"))
    if not abs_path.startswith(abs_base):
        raise PermissionError("Path Traversal attempt blocked")
    
    with open(abs_path, "rb") as f:
        return f.read()

def secure_hash_sha256(passwd: str):
    # Safe Cat 5: Using SHA-256 for secure hashing
    return hashlib.sha256(passwd.encode()).hexdigest()

def fetch_internal_api_safe():
    # Safe Cat 6: Accessing a static, safe local service URL
    return urllib.request.urlopen("http://localhost:8080/health")
