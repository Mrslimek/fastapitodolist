import jwt
from passlib.hash import pbkdf2_sha256
from app.config import settings
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from app.utils.exceptions import CustomDecodeError


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)


def encode_jwt(
    token_type: str,
    expire_timedelta: timedelta,
    payload: dict,
    private_key=settings.PRIVATE_KEY_PATH.read_text(),
    algorithm=settings.ALGORITHM,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)    
    expire = now + expire_timedelta
    to_encode.update(exp=expire, type=token_type, jti=str(uuid4()))
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise CustomDecodeError()
    return decoded


def create_access_token(username: str):
    jwt_payload = {"sub": username}
    return encode_jwt(
        payload=jwt_payload,
        token_type=settings.ACCESS_TOKEN_TYPE,
        expire_timedelta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(username: str):
    jwt_payload = {"sub": username}
    return encode_jwt(
        payload=jwt_payload,
        token_type=settings.REFRESH_TOKEN_TYPE,
        expire_timedelta=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )