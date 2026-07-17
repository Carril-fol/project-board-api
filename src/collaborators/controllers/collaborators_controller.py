from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from core.security.jwt_manager import jwt_required

from ..dependencies import get_collaborators_service
from ..schemas.collaborators_schema import (
    CollaboratorsOutputSchema,
    ListDetailCollaboratorsSchema,
)
from ..services.collaborators_service import CollaboratorService

router = APIRouter(prefix="/collaborators/api/v1", tags=["collaborators"])


@cbv(router)
class CollaboratorsController:
    service: CollaboratorService = Depends(get_collaborators_service)
    payload: dict = Depends(jwt_required)

    @router.get("/list/{id_project}", response_model=ListDetailCollaboratorsSchema)
    def get_collaborators(self, id_project: int):
        user_id = self.payload["sub"]

        return self.service.get_collaborators(id_project, user_id)

    @router.delete(
        "/delete/{id_collaborator}",
        response_model=CollaboratorsOutputSchema,
        status_code=200,
    )
    def remove_collaborator(self, id_collaborator: int):
        user_id = self.payload["sub"]

        self.service.remove_collaborator(id_collaborator, user_id)
        return CollaboratorsOutputSchema(msg="Collaborator removed")
