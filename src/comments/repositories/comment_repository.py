from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from ..models.comment_model import Comment


class CommentRepository(BaseRepository):
    
    def __init__(self, session):
        super().__init__(Comment, session)

    def get_comments_by_task_id(self, task_id: int):
        stmt = select(Comment).where(Comment.task_id == task_id)
        result = self.db.execute(stmt).scalars().all()
        return result