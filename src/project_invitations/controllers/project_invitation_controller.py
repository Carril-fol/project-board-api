from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv

from core.security.jwt_manager import jwt_required

from ..dependencies import get_project_invitation_service
from ..exceptions.project_invitation_exceptions import (
    InvitationAlreadyExistsError,
    InvitationNotFoundError,
)
from ..schemas.project_invitations_schemas import (
    CreateInvitationOutput,
    CreateProjectInvitation,
    ProjectInvitationOutput,
)
from ..services.project_invitations_service import ProjectInvitationService

router = APIRouter(prefix="/invitations/api/v1", tags=["invitations"])


@cbv(router)
class ProjectInvitationsController:
    service: ProjectInvitationService = Depends(get_project_invitation_service)
    payload: dict = Depends(jwt_required)

    @router.post(
        "/create",
        response_model=CreateInvitationOutput,
        status_code=201,
    )
    def create_invitation(self, data: CreateProjectInvitation):
        inviter_id = self.payload["sub"]

        try:
            token = self.service.create_project_invitation(data, inviter_id)
            return CreateInvitationOutput(
                msg="Invitation created successfully.",
                invite_url=f"http://localhost:8000{router.prefix}/{token}/respond",
            )
        
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))

        except InvitationAlreadyExistsError as error:
            raise HTTPException(status_code=409, detail=str(error))

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    @router.delete(
        "/remove/{id_invite}",
        response_model=ProjectInvitationOutput,
        status_code=200,
    )
    def remove_invitation(self, id_invite: int):
        user_id = self.payload["sub"]

        try:
            self.service.remove_project_invitation(id_invite, user_id)
            return ProjectInvitationOutput(msg="Invitation removed successfully.")

        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))

        except InvitationNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error))

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    @router.post(
        "/{token}/accept",
        response_model=ProjectInvitationOutput,
        status_code=200,
    )
    def accept_invitation(self, token: str):
        user_id = self.payload["sub"]

        try:
            self.service.respond_project_invitation(token, user_id, True)
            return ProjectInvitationOutput(msg="Invitation accepted successfully.")

        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))

        except InvitationNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error))

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    @router.post(
        "/{token}/reject",
        response_model=ProjectInvitationOutput,
        status_code=200,
    )
    def reject_invitation(self, token: str):
        user_id = self.payload["sub"]

        try:
            self.service.respond_project_invitation(token, user_id, False)

            return ProjectInvitationOutput(msg="Invitation rejected successfully.")

        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))

        except InvitationNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error))

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
