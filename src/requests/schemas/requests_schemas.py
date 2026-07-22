from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class RegisterRequestsInputSchema(BaseModel):
    message: Optional[str]
    role: str


class CreateRequestSchema(BaseModel):
    message: Optional[str]
    role: str
    project_id: int
    user_id: int
    status: RequestStatus = Field(default=RequestStatus.PENDING)

    @field_validator("role")
    @classmethod
    def upper_value(cls, v):
        return v.upper()

    @field_validator("project_id", "user_id")
    @classmethod
    def validate_ids(cls, v):
        if not v:
            raise ValueError("project_id and user_id cannot be empty")
        return v


class UpdateRequestSchema(BaseModel):
    status: RequestStatus


class DetailRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message: Optional[str]
    project_id: int
    user_id: int
    status: RequestStatus


class ListDetailRequestSchema(BaseModel):
    requests: list[DetailRequestSchema]


class RequestOutputSchema(BaseModel):
    msg: str
