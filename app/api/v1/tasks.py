from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.tasks import TaskResponseList, TaskResponse, TaskBase
from app.db.models.users import UserORM
from app.db.database import get_db
from app.services.auth import get_current_user
from app.services.tasks import (
    get_all_tasks,
    get_all_user_tasks,
    get_task_by_id,
    create_task_obj,
    save_task_in_db,
    update_task_obj,
    delete_task_from_db,
)


router = APIRouter(prefix="/tasks")


@router.get("/all", response_model=TaskResponseList)
async def list_tasks(
    db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    According to the tech task here we should accept only authorized clients
    but return all tasks from db
    """
    tasks_list = await get_all_tasks(db=db)
    return tasks_list


@router.get("/{task_id}", response_model=TaskResponse)
async def retrieve_task(
    task_id: int, db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    According to the tech task here we should accept only authorized clients
    but give any task from db, even not linked to user
    """
    task_obj = await get_task_by_id(db=db, task_id=task_id)
    return task_obj


@router.get("", response_model=TaskResponseList)
async def list_user_tasks(
    db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    According to the tech task here we should accept only authorized clients
    but return only tasks linked to exact user
    """
    tasks_list = await get_all_user_tasks(db=db, user_id=user_obj.id)
    return tasks_list


@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskBase,
    db: AsyncSession = Depends(get_db),
    user_obj: UserORM = Depends(get_current_user),
):
    """
    Here we create task with link to user,
    that was authorized during this creation
    """
    task_obj = create_task_obj(task_data=task_data.model_dump(), user_id=user_obj.id)
    await save_task_in_db(db=db, task_obj=task_obj)
    await db.refresh(task_obj)
    return task_obj


@router.patch("/{task_id}", response_model=TaskResponse)
async def partial_update_task(
    task_id: int,
    task_data: TaskBase,
    db: AsyncSession = Depends(get_db),
    user_obj: UserORM = Depends(get_current_user),
):
    """
    Here only authorized owner of the task can update it **IN WORK**
    """
    task_obj = await get_task_by_id(db=db, task_id=task_id)
    await update_task_obj(db=db, update_data=task_data.model_dump(), task_obj=task_obj)
    await db.refresh(task_obj)
    return task_obj


@router.delete("/{task_id}")
async def destroy_task(
    task_id: int, db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    Here only authorized owner of the task can destroy it **IN WORK**
    """
    task_obj = await get_task_by_id(db=db, task_id=task_id)
    await delete_task_from_db(db=db, task_obj=task_obj)
    return {"status": "success"}
