from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from core.security.jwt_manager import jwt_required

from ..dependencies import get_project_tag_service
from ..schemas.project_tag_schema import (
    ProjectTagOutputSchema,
    RegisterProjectTagInputSchema,
)
from ..services.project_tag_service import ProjectTagService

router = APIRouter(prefix="/projects-tags/api/v1", tags=["projects-tags"])


@cbv(router)
class ProjectTagController:
    service: ProjectTagService = Depends(get_project_tag_service)
    payload: dict = Depends(jwt_required)

    @router.post("/create", response_model=ProjectTagOutputSchema, status_code=201)
    def create_project_tag(
        self,
        id: int,
        data: RegisterProjectTagInputSchema,
    ):
        user_id = self.payload["sub"]

        try:
            self.service.create_project_tag(id, data, user_id)
            return ProjectTagOutputSchema(msg="Project tag created")
        except Exception as error:
            return ProjectTagOutputSchema(msg=str(error))

    @router.delete(
        "/delete/{id_tag}", response_model=ProjectTagOutputSchema, status_code=200
    )
    def delete_project_tag(
        self,
        id: int,
    ):
        user_id = self.payload["sub"]

        try:
            self.service.delete_tag_from_project(id, user_id)
            return ProjectTagOutputSchema(msg="Project tag deleted")
        except Exception as error:
            return ProjectTagOutputSchema(msg=str(error))
