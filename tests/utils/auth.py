from app.config import settings
from app.utils.auth import encode_jwt
import jwt
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from pathlib import Path


def create_test_access_token(username):
    payload = {
        "sub": username,
    }
    return encode_jwt(
        token_type=settings.ACCESS_TOKEN_TYPE,
        payload=payload,
        expire_timedelta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_test_refresh_token(
    username: str,
    token_type: str,
    expire_timedelta: timedelta,
    private_key: Path,
    algorithm: str,
    expired: bool
    ):
    payload = {
        "sub": username,
    }
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if not expired:
        expire = now + expire_timedelta
    else:
        expire = now - expire_timedelta
    to_encode.update(exp=expire, type=token_type, jti=str(uuid4()))
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded
    return jwt.encode
