from typing import List
from pydantic import BaseModel, RootModel
from app.utils.enums import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str
    status: TaskStatus
    
    model_config = {
        "extra": "forbid"
    }

class TaskResponse(TaskBase):
    id: int


class TaskResponseList(RootModel):
    root: List[TaskResponse]
