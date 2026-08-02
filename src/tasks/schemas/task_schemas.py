from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ..models.task_model import TaskPriority, TaskStatus


class TaskBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    expiration_date: Optional[datetime] = None


class RegisterTaskInputSchema(TaskBaseSchema):
    pass


class CreateTaskInputSchema(TaskBaseSchema):
    project_id: int


class UpdateTaskInputSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    expiration_date: Optional[datetime] = None


class DetailTaskOutputSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    expiration_date: Optional[datetime] = None
    project_id: int

    class Config:
        from_attributes = True


class ListDetailTaskOutputSchema(BaseModel):
    tasks: list[DetailTaskOutputSchema]


class TaskOutputSchema(BaseModel):
    msg: str


class AssignUserTaskInputSchema(BaseModel):
    user_id: int
