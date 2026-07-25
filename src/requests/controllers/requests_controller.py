from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_cache.decorator import cache

from core.security.jwt_manager import jwt_required
from shared.extensions import limiter

from ..dependencies import get_requests_service
from ..exceptions import (
    CollaboratorAlreadyExists,
    ProjectNotFoundError,
    RequestNotFound,
)
from ..schemas.requests_schemas import (
    DetailRequestSchema,
    ListDetailRequestSchema,
    RegisterRequestsInputSchema,
    RequestOutputSchema,
)
from ..services.requests_services import RequestsService

router = APIRouter(
    prefix="/requests/api/v1",
    tags=["requests"],
    dependencies=[Depends(jwt_required)],
)


@router.post(
    "/create/{project_id}",
    response_model=RequestOutputSchema,
    status_code=201,
)
@limiter.limit("10/minute")
def create(
    request: Request,
    data: RegisterRequestsInputSchema,
    project_id: int,
    service: RequestsService = Depends(get_requests_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    try:
        service.create_request(data, user_id, project_id)
        return RequestOutputSchema(msg="Request created successfully")
    except ProjectNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except CollaboratorAlreadyExists as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.post(
    "/approve/{request_id}",
    response_model=RequestOutputSchema,
    status_code=201,
)
@limiter.limit("10/minute")
def approve(
    request: Request,
    request_id: int,
    service: RequestsService = Depends(get_requests_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    try:
        service.respond_request(request_id, user_id, True)
        return RequestOutputSchema(msg="Request approved successfully")
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))
    except RequestNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post(
    "/decline/{request_id}",
    response_model=RequestOutputSchema,
    status_code=200,
)
@limiter.limit("10/minute")
def decline(
    request: Request,
    request_id: int,
    service: RequestsService = Depends(get_requests_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    try:
        service.respond_request(request_id, user_id, False)
        return RequestOutputSchema(msg="Request declined successfully")
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))
    except RequestNotFound as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    "/all/{project_id}",
    response_model=ListDetailRequestSchema,
    status_code=200,
)
@cache(expire=60)
@limiter.limit("10/minute")
async def get_all(
    request: Request,
    project_id: int,
    service: RequestsService = Depends(get_requests_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    try:
        requests = service.get_all_requests(project_id, user_id)
        return ListDetailRequestSchema(requests=requests)
    except ProjectNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))


@router.get(
    "/{request_id}",
    response_model=DetailRequestSchema,
    status_code=200,
)
@cache(expire=120)
@limiter.limit("10/minute")
async def get_request(
    request: Request,
    request_id: int,
    service: RequestsService = Depends(get_requests_service),
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    request = service.get_request(request_id, user_id)
    return request
