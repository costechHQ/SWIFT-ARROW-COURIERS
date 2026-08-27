import hashlib
import secrets
import time

active_tokens = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash

def generate_token():
    return secrets.token_urlsafe(32)


def login(username, password, staff):
    """Authenticates a staff member and generates a secure session token."""

    for user in staff:
        if user["username"] == username:
            if verify_password(password, user["password_hash"]):
                token = generate_token()

                active_tokens[token] = {
                    "username": user["username"],
                    "position": user["position"],
                    "issued_at": time.time()
                }

                return token
            
            return None
        
    return None

def validate_token(token):
    """validates a session token and retrieves the associated staff data"""
    session = active_tokens.get(token)

    if session is None:
        return None

    return session

def logout(token):
    """terminates an active staff session b y removing its token"""
    if token in active_tokens:
        del active_tokens[token]
        return True
    return False

def can_delete(session):
    return session["position"] == "Station Master"