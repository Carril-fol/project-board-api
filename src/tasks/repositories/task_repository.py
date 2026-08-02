from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from ..models.task_model import Task
from ..models.task_user_model import TaskUser

class TaskRepository(BaseRepository[Task]):

    def __init__(self, db):
        super().__init__(Task, db)

    def get_tasks_by_project(self, project_id: int):
        return self.db.execute(
            select(self.model).
            where(self.model.project_id == project_id)
        ).scalars().all()

    def assign_user(self, task_id: int, user_id: int):
        stmt = select(TaskUser).where(
            TaskUser.task_id == task_id,
            TaskUser.user_id == user_id
        )
        existing = self.db.execute(stmt).scalar_one_or_none()
        if existing:
            return existing

        assignment = TaskUser(task_id=task_id, user_id=user_id)
        super().create(assignment)
        return assignment

    def unassign_user(self, task_id: int, user_id: int):
        stmt = select(TaskUser).where(
            TaskUser.task_id == task_id,
            TaskUser.user_id == user_id
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        if result:
            self.db.delete(result)
            self.db.commit()
            return True
        return False

    def get_tasks_from_user(self, user_id: int):
        stmt = select(Task).join(TaskUser).where(TaskUser.user_id == user_id)
        return self.db.execute(stmt).scalars().all()

    def get_tasks_with_priority(self, priority: str):
        stmt = select(Task).where(Task.priority == priority)
        return self.db.execute(stmt).scalars().all()

    def get_tasks_by_title_or_description(self, search_term: str):
        stmt = select(Task).where(
            (Task.title.ilike(f"%{search_term}%")) |
            (Task.description.ilike(f"%{search_term}%"))
        )
        return self.db.execute(stmt).scalars().all()

    def get_tasks_by_status(self, status: str):
        stmt = select(Task).where(Task.status == status)
        return self.db.execute(stmt).scalars().all()
