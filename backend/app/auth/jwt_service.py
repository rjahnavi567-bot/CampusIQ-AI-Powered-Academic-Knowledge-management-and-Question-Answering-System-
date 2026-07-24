from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "AcademicSystemSecretKey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data):

    payload = data.copy()

    payload["exp"] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None