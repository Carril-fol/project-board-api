from fastapi import APIRouter, Depends, Request
from fastapi_cache.decorator import cache

from core.security.jwt_manager import jwt_required
from shared.extensions import limiter

from ..dependencies import get_collaborators_service
from ..schemas.collaborators_schema import (
    CollaboratorsOutputSchema,
    ListDetailCollaboratorsSchema,
)
from ..services.collaborators_service import CollaboratorService

router = APIRouter(prefix="/collaborators/api/v1", tags=["collaborators"])


@router.get(
    "/get/{project_id}",
    response_model=ListDetailCollaboratorsSchema,
    status_code=200,
)
@cache(expire=10)
@limiter.limit("10/minute")
def get_collaborators(
    request: Request,
    project_id: int,
    service: CollaboratorService = Depends(get_collaborators_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    return service.get_collaborators(project_id, user_id)


@router.delete(
    "/delete/{id_collaborator}",
    response_model=CollaboratorsOutputSchema,
    status_code=200,
)
@limiter.limit("10/minute")
def remove_collaborator(
    request: Request,
    id_collaborator: int,
    service: CollaboratorService = Depends(get_collaborators_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]

    service.remove_collaborator(id_collaborator, user_id)
    return CollaboratorsOutputSchema(msg="Collaborator removed")
