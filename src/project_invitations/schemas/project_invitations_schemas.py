from pydantic import BaseModel, Field, field_validator


class ProjectInvitationBase(BaseModel):
    id_project: int = Field(gt=0)
    id_invitee: int = Field(gt=0)
    role: str = Field(min_length=1, max_length=100)


class CreateProjectInvitation(ProjectInvitationBase):
    pass

    @field_validator("role", mode="before")
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class RespondInvitationInput(BaseModel):
    id_invitation: int
    accept: bool


class CreateInvitationOutput(BaseModel):
    msg: str
    invite_url: str


class ProjectInvitationOutput(BaseModel):
    msg: str
