from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.models.tasks import TaskORM
from app.utils.exceptions import RecordNotFound


async def get_all_tasks(db: AsyncSession) -> List[TaskORM] | List:
    """
    function for business logic
    Getting all tasks from db
    returning list of TaskORM models
    """
    result = await db.scalars(select(TaskORM))
    tasks_list = result.all()
    return tasks_list


async def get_all_user_tasks(db: AsyncSession, user_id: int) -> List[TaskORM] | List:
    """
    function, similar to 'get_all_tasks'
    but with additional parameter "user_id"
    to get tasks for exact user
    """
    result = await db.scalars(select(TaskORM).where(TaskORM.user_id == user_id))
    tasks_list = result.all()
    return tasks_list


async def get_task_by_id(db: AsyncSession, task_id: int) -> TaskORM:
    task_obj = await db.get(TaskORM, task_id)
    if not task_obj:
        raise RecordNotFound(model="task", model_id=task_id) 
    return task_obj


def create_task_obj(task_data: dict, user_id: int) -> TaskORM:
    task_obj = TaskORM(**task_data, user_id=user_id)
    return task_obj


async def save_task_in_db(db: AsyncSession, task_obj: TaskORM) -> None:
    db.add(task_obj)
    await db.commit()


async def update_task_obj(db: AsyncSession, update_data: dict, task_obj: TaskORM) -> None:
    for key, value in update_data.items():
        if key and value:
            setattr(task_obj, key, value)
    await db.commit()


async def delete_task_from_db(db: AsyncSession, task_obj: TaskORM) -> None:
    await db.delete(task_obj)
    await db.commit()


async def filter_tasks_by_status(db: AsyncSession, task_status: str = None) -> List[TaskORM]:
    tasks_list = await db.scalars(select(TaskORM).where(TaskORM.status == task_status))
    return tasks_list


def check_task_owner(db: AsyncSession, task_obj: TaskORM, user_id: int):
    if task_obj.user_id == user_id:
        return True
    return False
