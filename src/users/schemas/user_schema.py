from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    bio: str
    email: str

    model_config = {
        "from_attributes": True
    }