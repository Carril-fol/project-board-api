from sqlalchemy.orm import Session

from ..models.project_invitation_model import ProjectInvitation


class ProjectInvitationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project_invitation(self, project_invitation: ProjectInvitation):
        self.db.add(project_invitation)
        self.db.flush()
        return project_invitation

    def get_invite_by_project_id_and_invitee_id(self, project_id: int, invitee_id: int):
        return (
            self.db.query(ProjectInvitation)
            .filter(
                ProjectInvitation.id_project == project_id,
                ProjectInvitation.id_invitee == invitee_id,
            )
            .first()
        )

    def get_invite_by_id(self, id: int):
        return (
            self.db.query(ProjectInvitation).filter(ProjectInvitation.id == id).first()
        )

    def delete_project_invitation(self, project_invitation: ProjectInvitation):
        self.db.delete(project_invitation)
        self.db.flush()

    def get_by_token(self, token: str):
        return (
            self.db.query(ProjectInvitation)
            .filter(ProjectInvitation.token == token)
            .first()
        )

    def get_project_invitation_by_project_id_and_user_id(
        self, project_id: int, user_id: int
    ):
        return (
            self.db.query(ProjectInvitation)
            .filter(
                ProjectInvitation.id_project == project_id,
                ProjectInvitation.id_invitee == user_id,
            )
            .all()
        )
