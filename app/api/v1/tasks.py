from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import paginate
from app.schemas.tasks import TaskResponseList, TaskResponse, TaskBase, TaskPartialUpdate
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
    filter_tasks_by_status,
    check_task_owner,
)
from app.utils.enums import TaskStatus
from app.utils.exceptions import RecordNotFound
from app.utils.pagination import Page


router = APIRouter(prefix="/tasks")


@router.get("/all", response_model=Page[TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    According to the tech task here we should accept only authorized clients
    but return all tasks from db paginated
    """
    tasks_list = await get_all_tasks(db=db)
    return paginate(tasks_list)


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


@router.get("", response_model=Page[TaskResponse])
async def list_user_tasks(
    db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    According to the tech task here we should accept only authorized clients
    but return only tasks linked to exact user
    """
    tasks_list = await get_all_user_tasks(db=db, user_id=user_obj.id)
    return paginate(tasks_list)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
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
    task_data: TaskPartialUpdate,
    db: AsyncSession = Depends(get_db),
    user_obj: UserORM = Depends(get_current_user),
):
    """
    Here only authorized owner of the task can update it **IN WORK**
    """
    task_obj = await get_task_by_id(db=db, task_id=task_id)
    if check_task_owner(db=db, task_obj=task_obj, user_id=user_obj.id):
        await update_task_obj(db=db, update_data=task_data.model_dump(), task_obj=task_obj)
        await db.refresh(task_obj)
        return task_obj
    else:
        raise RecordNotFound()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_task(
    task_id: int, db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    Here only authorized owner of the task can destroy it **IN WORK**
    """
    task_obj = await get_task_by_id(db=db, task_id=task_id)
    if check_task_owner(db=db, task_obj=task_obj, user_id=user_obj.id):
        await delete_task_from_db(db=db, task_obj=task_obj)
    else:
        raise RecordNotFound()


@router.post("/{task_id}", response_model=TaskResponse)
async def mark_task_as_completed(
    task_id: int, db: AsyncSession = Depends(get_db), user_obj: UserORM = Depends(get_current_user)
):
    """
    Mark given task as completed. Section 4 of tech task
    """
    task_obj = await get_task_by_id(db=db, task_id=task_id)
    if check_task_owner(db=db, task_obj=task_obj, user_id=user_obj.id):
        await update_task_obj(
            db=db, update_data={"status": TaskStatus.COMPLETED}, task_obj=task_obj
        )
        await db.refresh(task_obj)
        return task_obj
    else:
        raise RecordNotFound()


@router.get("/filter/", response_model=TaskResponseList)
async def get_tasks_filtered_by_status(
    task_status: TaskStatus = None,
    db: AsyncSession = Depends(get_db),
    user_obj: UserORM = Depends(get_current_user),
):
    """
    Filter tasks by status. Section 4 of teck task
    """
    if task_status:
        tasks_list = await filter_tasks_by_status(db=db, task_status=task_status)
    else:
        tasks_list = await get_all_tasks(db=db)
    return tasks_list
