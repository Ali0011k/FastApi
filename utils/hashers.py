import secrets
import hashlib


def hash_password(password: str):
    """hash password that is given"""

    hashed_password = hashlib.sha256((password).encode("utf-8")).hexdigest()
    return hashed_password


def verify_password(password, hashed_password):
    """verify password is equals with hashed password"""

    hashed_input_password = hashlib.sha256((password).encode("utf-8")).hexdigest()
    print(hashed_input_password)
    return hashed_input_password == hashed_password
