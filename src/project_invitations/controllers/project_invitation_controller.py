from fastapi import APIRouter, Depends

from core.security.jwt_manager import jwt_required

from ..dependencies import get_project_invitation_service
from ..schemas.project_invitations_schemas import (
    CreateInvitationOutput,
    CreateProjectInvitation,
    ProjectInvitationOutput,
)
from ..services.project_invitations_service import ProjectInvitationService

router = APIRouter(
    prefix="/invitations/api/v1",
    tags=["invitations"],
    dependencies=[Depends(jwt_required)],
)


@router.post("/create", response_model=CreateInvitationOutput, status_code=201)
def create_invitation(
    data: CreateProjectInvitation,
    service: ProjectInvitationService = Depends(get_project_invitation_service),
    payload: dict = Depends(jwt_required),
):
    inviter_id = payload["sub"]
    token = service.create_project_invitation(data, inviter_id)
    return CreateInvitationOutput(
        msg="Invitation created successfully.",
        token=token,
        accept_url=f"{router.prefix}/{token}/accept",
        reject_url=f"{router.prefix}/{token}/reject",
    )


@router.delete(
    "/remove/{id_invite}", response_model=ProjectInvitationOutput, status_code=200
)
def remove_invitation(
    id_invite: int,
    service: ProjectInvitationService = Depends(get_project_invitation_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]

    service.remove_project_invitation(id_invite, user_id)
    return ProjectInvitationOutput(msg="Invitation removed successfully.")


@router.post("/{token}/accept", response_model=ProjectInvitationOutput, status_code=200)
def accept_invitation(
    token: str,
    service: ProjectInvitationService = Depends(get_project_invitation_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]

    service.respond_project_invitation(token, user_id, True)
    return ProjectInvitationOutput(msg="Invitation accepted successfully.")


@router.post("/{token}/reject", response_model=ProjectInvitationOutput, status_code=200)
def reject_invitation(
    token: str,
    service: ProjectInvitationService = Depends(get_project_invitation_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]

    service.respond_project_invitation(token, user_id, False)
    return ProjectInvitationOutput(msg="Invitation rejected successfully.")
