from jose import jwt
from decouple import config


SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = config("ALGORITHM", str)


def encode_jwt(user):
    """encoding token that given"""

    token = jwt.encode(
        user,
        SECRET_KEY,
        ALGORITHM,
    )
    return token


def decode_jwt(token):
    """decode token that given"""

    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return user.get("id")
    except jwt.JWTError as e:
        return None
