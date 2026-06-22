import string
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class RegisterInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    bio: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=15)
    confirm_password: str = Field(min_length=8, max_length=15)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        if not any(char in string.punctuation for char in value):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial"
            )
        return value
    
    @model_validator(mode="after")
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Password not match")
        return self
    

class RegisterOutputSchema(BaseModel):
    msg: str = Field(..., examples=["Register successfully"])


class LoginInputSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        if not any(char in string.punctuation for char in value):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial"
            )
        return value


class LoginOutputSchema(BaseModel):
    access_token: str
    refresh_token: str
    

class LogoutOutputSchema(BaseModel):
    msg: str = Field(..., examples=["Logout successfully"])


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    bio: str
    email: EmailStr
    password: str
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @field_validator("first_name", "last_name", "username", "bio", mode='before')
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    