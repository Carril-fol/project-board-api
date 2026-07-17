from pydantic import BaseModel, field_validator

from users.schemas.user_schema import UserResponse


class RegisterCollaboratorsInputSchema(BaseModel):
    role: str
    id_project: int
    id_user: int


class CreateCollaboratorsSchema(BaseModel):
    role: str
    id_project: int
    id_user: int

    @field_validator("role", mode="before")
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class DetailCollaboratorsSchema(BaseModel):
    role: str
    user: UserResponse

    model_config = {"from_attributes": True}


class ListDetailCollaboratorsSchema(BaseModel):
    collaborators: list[DetailCollaboratorsSchema]


class CollaboratorsOutputSchema(BaseModel):
    msg: str
