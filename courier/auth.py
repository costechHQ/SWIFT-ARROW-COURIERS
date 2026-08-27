import hashlib
import secrets
import time

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash

def generate_token():
    return secrets.token_urlsafe(32)