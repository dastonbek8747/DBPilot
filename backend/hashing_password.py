from uuid import uuid4

from argon2 import PasswordHasher

hasher = PasswordHasher()


def generate_session_id():
    return str(uuid4())


def hashing_password(password):
    return hasher.hash(password)


def verify_password(password, hashed_password):
    try:
        return bool(hasher.verify(hashed_password, password))
    except Exception:
        return False
