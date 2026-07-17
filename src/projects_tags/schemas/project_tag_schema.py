from pydantic import BaseModel, Field, field_validator

class RegisterProjectTagInputSchema(BaseModel):
    tag: str = Field(min_length=3, max_length=100)


class ProjectTagOutputSchema(BaseModel):
    msg: str


class CreateProjectTag(BaseModel):
    id_project: int
    tag: str

    @field_validator("tag", mode='before')
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value