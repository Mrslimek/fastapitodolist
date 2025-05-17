from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from app.utils.auth import verify_password, decode_jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.auth import RevokedTokenORM
from app.schemas.users import UserLogin
from app.db.models.users import UserORM
from app.db.database import get_db
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_user_by_username(username: str, db: AsyncSession) -> UserORM:
    result = await db.scalars(select(UserORM).where(UserORM.username == username))
    user_obj = result.one_or_none()
    return user_obj


async def validate_user(user_data: UserLogin, db: AsyncSession = Depends(get_db)) -> UserORM:
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )
    user_obj = await get_user_by_username(db=db, username=user_data.username)
    if not user_obj or not verify_password(
        password=user_data.password, hashed_password=user_obj.password
    ):
        raise unauthed_exception
    return user_obj


def get_refresh_token_and_payload(request: Request) -> dict:
    refresh_token = request.cookies.get("refresh")
    payload = decode_jwt(token=refresh_token)
    token_type = payload.get("type")
    if not token_type == settings.REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token type is not '{settings.REFRESH_TOKEN_TYPE}'",
        )
    return payload


async def validate_refresh_token(
    db: AsyncSession = Depends(get_db), payload: dict = Depends(get_refresh_token_and_payload)
) -> UserORM:
    jti = payload.get("jti")
    if not await is_token_in_blacklist(db=db, jti=jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is in blacklist"
        )
    username = payload.get("sub")
    user_obj = await get_user_by_username(username=username, db=db)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return user_obj


def get_access_token_and_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    # TODO: При неудаче отдает 500-ую
    payload = decode_jwt(token=token)
    token_type = payload.get("type")
    if not token_type == settings.ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token type is not '{settings.ACCESS_TOKEN_TYPE}'",
        )
    return payload


async def get_current_user(
    payload: dict = Depends(get_access_token_and_payload), db: AsyncSession = Depends(get_db)
) -> UserORM:
    jti = payload.get("jti")
    if not await is_token_in_blacklist(db=db, jti=jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is in blacklist"
        )
    username: str = payload.get("sub")
    user_obj = await get_user_by_username(db=db, username=username)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return user_obj


def get_access_refresh_tokens_jti(
    refresh_token_payload: dict = Depends(get_refresh_token_and_payload),
    access_token_payload: dict = Depends(get_access_token_and_payload),
) -> tuple:
    refresh_token_jti = refresh_token_payload.get("jti")
    access_token_jti = access_token_payload.get("jti")
    return (refresh_token_jti, access_token_jti)


async def blacklist_access_refresh_token(db: AsyncSession, jti_tuple: tuple) -> None:
    revoked_tokens = [RevokedTokenORM(jti=jti) for jti in jti_tuple]
    async with db.begin():
        db.add_all(revoked_tokens)


async def is_token_in_blacklist(db: AsyncSession, jti: str) -> bool:
    return await db.get(RevokedTokenORM, jti) is None
