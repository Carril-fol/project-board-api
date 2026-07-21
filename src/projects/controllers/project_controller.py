from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv

from core.security.jwt_manager import jwt_required

from ..dependencies import get_project_service
from ..exceptions.project_exception import (
    ProjectAlreadyHasStatus,
    ProjectInsufficientPrivileges,
    ProjectNotFound,
)
from ..schemas.project_schema import (
    DeleteProjectOutputSchema,
    ListProjectDetail,
    ProjectDetail,
    RegisterProjectInputSchema,
    RegisterProjectOutputSchema,
    UpdateProjectInputSchema,
    UpdateProjectOutputSchema,
)
from ..services.project_service import ProjectService

router = APIRouter(prefix="/projects/api/v1", tags=["projects"])


@cbv(router)
class ProjectController:
    service: ProjectService = Depends(get_project_service)
    payload: dict = Depends(jwt_required)

    @router.post("/create", response_model=RegisterProjectOutputSchema, status_code=201)
    async def create_project(self, data: RegisterProjectInputSchema):
        user_id = self.payload["sub"]

        self.service.create_project(data, user_id)
        return RegisterProjectOutputSchema(msg="Project created successfully")

    @router.get("/get/{id}", response_model=ProjectDetail, status_code=200)
    async def get_project(self, id: int):
        try:
            project = self.service.detail_project_by_id(id)
            return project
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found.")

    @router.patch(
        "/update/{id}", response_model=UpdateProjectOutputSchema, status_code=200
    )
    async def update_project(self, id: int, data: UpdateProjectInputSchema):
        try:
            user_id = self.payload["sub"]

            self.service.update_project(id, data, user_id)
            return UpdateProjectOutputSchema(msg="Project updated")
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found.")
        except ProjectInsufficientPrivileges:
            raise HTTPException(
                status_code=404, detail="You don't have privileges for this action."
            )

    @router.delete(
        "/delete/{id}", response_model=DeleteProjectOutputSchema, status_code=200
    )
    async def delete_project(self, id: int):
        try:
            user_id = self.payload["sub"]
            data = {"status": "CANCELLED"}

            self.service.delete_project(id, user_id, data)
            return DeleteProjectOutputSchema(msg="Project deleted successfully")
        except ProjectNotFound:
            raise HTTPException(status_code=404, detail="Project not found.")
        except ProjectInsufficientPrivileges:
            raise HTTPException(
                status_code=403, detail="You don't have privileges for this action."
            )
        except ProjectAlreadyHasStatus:
            raise HTTPException(
                status_code=409, detail="The project has already been cancelled."
            )

    @router.get("/", response_model=ListProjectDetail, status_code=200)
    async def get_all_project(self, per_page: int = 10, page: int = 1):
        list_detailed_projects = self.service.get_all_project(per_page, page)
        return list_detailed_projects
