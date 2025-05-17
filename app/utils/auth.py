import jwt
from passlib.hash import pbkdf2_sha256
from app.config import settings
from datetime import datetime, timedelta


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)


def encode_jwt(
    expire_minutes: int,
    payload: dict,
    private_key=settings.PRIVATE_KEY_PATH.read_text(),
    algorithm=settings.ALGORITHM,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire)
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
