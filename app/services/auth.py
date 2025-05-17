from fastapi import HTTPException, Form, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import UserORM
from app.db.database import get_db
from app.utils.auth import verify_password, decode_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(username: str, password: str, first_name: str, last_name: str | None) -> UserORM:
    user_obj = UserORM.create(
        username=username, password=password, first_name=first_name, last_name=last_name
    )
    return user_obj


async def save_user_in_db(db: AsyncSession, user_obj: UserORM) -> None:
    async with db.begin():
        db.add(user_obj)


async def get_user_by_username(
    username: str, db: AsyncSession, user_class: type[UserORM]
) -> UserORM:
    result = await db.scalars(select(UserORM).where(UserORM.username == username))
    user_obj = result.one_or_none()
    return user_obj


async def validate_user(
    username: str = Form(), password: str = Form(), db: AsyncSession = Depends(get_db)
) -> UserORM:
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )
    user_obj = await get_user_by_username(db=db, user_class=UserORM, username=username)
    if not user_obj:
        raise unauthed_exception
    if not verify_password(password=password, hashed_password=user_obj.password):
        raise unauthed_exception
    return user_obj


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    # TODO: При неудаче отдает 500-ую
    payload = decode_jwt(token=token)
    return payload


async def get_current_user(
    payload: dict = Depends(get_current_token_payload), db: AsyncSession = Depends(get_db)
) -> UserORM:
    username: str = payload.get("sub")
    user_obj = await get_user_by_username(db=db, user_class=UserORM, username=username)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found")
    return user_obj
