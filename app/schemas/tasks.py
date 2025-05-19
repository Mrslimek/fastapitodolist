from typing import List
from pydantic import BaseModel, RootModel, ConfigDict
from app.utils.enums import TaskStatus
from app.utils.schemas import NonEmptyString


class TaskBase(BaseModel):
    title: NonEmptyString
    description: NonEmptyString | None = None
    status: TaskStatus = TaskStatus.NEW

    model_config = ConfigDict(extra="forbid")


class TaskPartialUpdate(BaseModel):
    title: NonEmptyString | None = None
    description: NonEmptyString | None = None
    status: TaskStatus | None = None

    model_config = ConfigDict(extra="forbid")


class TaskResponse(TaskBase):
    id: int


class TaskResponseList(RootModel):
    root: List[TaskResponse]
