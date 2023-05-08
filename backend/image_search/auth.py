from datetime import datetime, timedelta
import typing

from jose import JWTError, jwt
from passlib.context import CryptContext

from . import logs

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logs.get_logger()


def create_access_token(
    data: dict,
    secret: str,
    expires_delta: typing.Optional[timedelta] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return encoded_jwt


def decode_username(token: str, secret: str) -> typing.Optional[str]:
    username = None
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        logger.exception("Failed to decode JWT")
        pass

    return username


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)
