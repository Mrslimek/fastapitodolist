from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import UserORM


def create_user(username: str, password: str, first_name: str, last_name: str | None) -> UserORM:
    user_obj = UserORM.create(
        username=username, password=password, first_name=first_name, last_name=last_name
    )
    return user_obj


async def save_user_in_db(db: AsyncSession, user_obj: UserORM) -> None:
    async with db.begin():
        db.add(user_obj)
