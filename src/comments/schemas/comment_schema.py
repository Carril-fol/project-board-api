from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CommentBaseSchema(BaseModel):
    content: str = Field(..., description="The content of the comment")
    task_id: int = Field(..., description="The ID of the task associated with the comment")
    user_id: int = Field(..., description="The ID of the user who created the comment")
    
    class Config:
        from_attributes = True


class RegisterCommentInputSchema(BaseModel):
    content: str = Field(..., description="The content of the comment")        


class CreateCommentSchema(CommentBaseSchema):
    pass


class DetailCommentOutputSchema(CommentBaseSchema):
    id: int = Field(..., description="The ID of the comment")
    content: str = Field(..., description="The content of the comment")
    created_at: datetime = Field(..., description="The timestamp when the comment was created")
    updated_at: datetime = Field(..., description="The timestamp when the comment was last updated")
    
    model_config = ConfigDict(from_attributes=True)
    
    
class ListDetailCommentOutputSchema(BaseModel):
    comments: list[DetailCommentOutputSchema] = Field(..., description="List of comments")
    total: int = Field(..., description="Total number of comments")
    limit: int = Field(..., description="Number of comments per page")
    offset: int = Field(..., description="Current offset")
    

class UpdateCommentSchema(BaseModel):
    content: str = Field(..., description="The content of the comment")        


class CommentOutputSchema(BaseModel):
    msg: str = Field(..., description="A message indicating the result of the operation")