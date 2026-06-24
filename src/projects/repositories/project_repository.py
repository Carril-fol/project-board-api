from sqlalchemy.orm import Session
from ..models.project import Project

class ProjectRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.flush()
        return project

    def get_project_by_id(self, id: int) -> Project | None:
        return self.db.query(Project).filter(Project.id == id).first()
    
    def update(self, project: Project) -> Project:
        self.db.flush()
        self.db.refresh(project)
        return project
    
    def delete_logic(self, project: Project) -> Project:
        return self.update(project)
    
    def get_all_project(self, per_page: int, page: int) -> list[Project]:
        query = self.db.query(Project)

        total = query.count()
        projects = query.offset((page - 1) * per_page).limit(per_page).all()

        return projects, total