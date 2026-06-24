from fastapi import APIRouter, HTTPException, Request, Depends

from core.security.jwt_manager import JwtManager

from ..dependencies import get_project_service
from ..services.project_service import ProjectService
from ..exceptions.project_exception import ProjectNotFound, ProjectInsufficientPrivileges, ProjectAlreadyHasStatus
from ..schemas.project_schema import (
    RegisterProjectInputSchema, 
    RegisterProjectOutputSchema, 
    UpdateProjectInputSchema,
    UpdateProjectOutputSchema,
    DeleteProjectOutputSchema,
    ProjectDetail,
    ListProjectDetail
)


router = APIRouter(
    prefix="/projects/api/v1", 
    tags=["projects"]
)


@router.post(
    "/create",
    response_model=RegisterProjectOutputSchema,
    status_code=201
)
async def create_project(
    request: Request,
    data: RegisterProjectInputSchema,
    project_service: ProjectService = Depends(get_project_service),
    jwt_manager: JwtManager = Depends()
):
    token = request.cookies.get("access_token")
    user_id = jwt_manager.decode_token(token)["sub"]

    project_service.create_project(data, user_id)
    return RegisterProjectOutputSchema(msg="Project created successfully")


@router.get(
    "/get/{id}",
    response_model=ProjectDetail,
    status_code=200
)
async def get_project(
    id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    try:
        project = project_service.detail_project_by_id(id)
        return project
    except ProjectNotFound:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )


@router.patch(
    "/update/{id}",
    response_model=UpdateProjectOutputSchema,
    status_code=200
)
async def update_project(
    id: int,
    request: Request,
    data: UpdateProjectInputSchema,
    project_service: ProjectService = Depends(get_project_service),
    jwt_manager: JwtManager = Depends()
):
    try:
        token = request.cookies.get("access_token")
        user_id = int(jwt_manager.decode_token(token)["sub"])

        project_service.update_project(id, data, user_id)
        return UpdateProjectOutputSchema(msg="Project updated")
    except ProjectNotFound:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )
    except ProjectInsufficientPrivileges:
        raise HTTPException(
            status_code=404,
            detail="You don't have privileges for this action."
        )
    

@router.delete(
    "/delete/{id}",
    response_model=DeleteProjectOutputSchema,
    status_code=200
)
async def delete_project(
    id: int,
    request: Request,
    project_service: ProjectService = Depends(get_project_service),
    jwt_manager: JwtManager = Depends()
):
    try:
        token = request.cookies.get("access_token")
        user_id = int(jwt_manager.decode_token(token)["sub"])
        data = {"status": "CANCELLED"}
        
        project_service.delete_project(id, user_id, data)
        return DeleteProjectOutputSchema(msg="Project deleted successfully")
    except ProjectNotFound:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )
    except ProjectInsufficientPrivileges:
        raise HTTPException(
            status_code=403,
            detail="You don't have privileges for this action."
        )
    except ProjectAlreadyHasStatus:
        raise HTTPException(
            status_code=409,
            detail="The project has already been cancelled."
        )
    

@router.get(
    "/",
    response_model=ListProjectDetail,
    status_code=200
)
async def get_all_project(
    per_page: int = 10, 
    page: int = 1,
    project_service: ProjectService = Depends(get_project_service),
):
    list_detailed_projects = project_service.get_all_project(per_page, page)
    return list_detailed_projects