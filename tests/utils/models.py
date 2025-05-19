from app.db.models.tasks import TaskORM
from sqlalchemy.ext.asyncio import AsyncSession
import random
import string


async def setup_test_task(db: AsyncSession):
    new_task = TaskORM(title="Test Task", status="New", user_id=1)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task.id


def random_string(length: int = 10) -> str:
    """
    Here we generate random string for test purposes.
    Because i didn't want to add Faker dependency to the project
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))