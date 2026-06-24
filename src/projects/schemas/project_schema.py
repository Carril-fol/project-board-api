from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator, Field


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RegisterProjectInputSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    status: ProjectStatus
    description: str = Field(min_length=10, max_length=500)
    max_collaborators: int = Field(gt=0)


class RegisterProjectOutputSchema(BaseModel):
    msg: str = Field(..., examples=["Project created successfully"])


class UpdateProjectInputSchema(BaseModel):
    name: Optional[str] = None
    status: Optional[ProjectStatus] = None
    description: Optional[str] = None
    max_collaborators: Optional[int] = None


class UpdateProjectOutputSchema(BaseModel):
    msg: str = Field(..., examples=["Project updated successfully"])


class DeleteProjectOutputSchema(BaseModel):
    msg: str = Field(..., examples=["Project deleted successfully"])


class ProjectCreateSchema(BaseModel):
    name: str
    status: str
    description: str = Field(min_length=10, max_length=500)
    max_collaborators: int = Field(gt=0)
    owner_id: int

    @field_validator("name", "status", mode='before')
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

class ProjectUpdateSchema(BaseModel):
    name: Optional[str] = None
    status: Optional[ProjectStatus] = None
    description: Optional[str] = None
    max_collaborators: Optional[int] = None
    owner_id: int

    @field_validator("name", "status", mode='before')
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class ProjectDetail(BaseModel):    
    name: str
    status: str
    description: str
    max_collaborators: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ListProjectDetail(BaseModel):
    projects: list[ProjectDetail]
    total: int