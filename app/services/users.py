from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import UserORM


async def get_user_by_username(username: str, db: AsyncSession) -> UserORM:
    result = await db.scalars(select(UserORM).where(UserORM.username == username))
    user_obj = result.one_or_none()
    return user_obj


def create_user(username: str, password: str, first_name: str, last_name: str | None) -> UserORM:
    user_obj = UserORM.create(
        username=username, password=password, first_name=first_name, last_name=last_name
    )
    return user_obj


async def save_user_in_db(db: AsyncSession, user_obj: UserORM) -> None:
    db.add(user_obj)
    await db.commit()


async def is_username_available(db: AsyncSession, username: str) -> bool:
    user_obj = await get_user_by_username(db=db, username=username)
    if not user_obj:
        return True
    else:
        return False
