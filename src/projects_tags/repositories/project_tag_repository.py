from sqlalchemy.orm import Session

from ..models.project_tag_model import ProjectTag


class ProjectTagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_tag: ProjectTag) -> ProjectTag:
        self.db.add(project_tag)
        self.db.flush()
        return project_tag

    def update(self, project_tag: ProjectTag) -> ProjectTag:
        self.db.flush()
        self.db.refresh(project_tag)
        return project_tag

    def delete_logic(self, project_tag: ProjectTag) -> ProjectTag:
        return self.update(project_tag)

    def get_project_tag_by_id(self, id: int) -> ProjectTag | None:
        return self.db.query(ProjectTag).filter(ProjectTag.id == id).first()

    def delete(self, project_tag: ProjectTag):
        self.db.delete(project_tag)
        self.db.flush()
        return project_tag
