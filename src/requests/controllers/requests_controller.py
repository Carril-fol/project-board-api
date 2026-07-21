from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv

from collaborators.exceptions import CollaboratorAlreadyExists
from core.security.jwt_manager import jwt_required
from projects.exceptions.project_exception import ProjectNotFound

from ..dependencies import get_requests_service
from ..exceptions import RequestNotFound
from ..schemas.requests_schemas import (
    DetailRequestSchema,
    ListDetailRequestSchema,
    RegisterRequestsInputSchema,
    RequestOutputSchema,
)
from ..services.requests_services import RequestsService

router = APIRouter(prefix="/requests/api/v1", tags=["requests"])


@cbv(router)
class RequestsController:
    service: RequestsService = Depends(get_requests_service)
    payload: dict = Depends(jwt_required)

    @router.post(
        "/create/{project_id}",
        response_model=RequestOutputSchema,
        status_code=201,
    )
    def create(self, data: RegisterRequestsInputSchema, project_id: int):
        user_id = self.payload["sub"]

        try:
            self.service.create_request(data, user_id, project_id)
            return RequestOutputSchema(msg="Request created successfully")

        except ProjectNotFound as error:
            raise HTTPException(status_code=404, detail=str(error))
        except CollaboratorAlreadyExists as error:
            raise HTTPException(status_code=404, detail=str(error))
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    @router.post(
        "/approve/{request_id}",
        response_model=RequestOutputSchema,
        status_code=200,
    )
    def approve(self, request_id: int):
        user_id = self.payload["sub"]

        try:
            self.service.respond_request(request_id, user_id, True)
            return RequestOutputSchema(msg="Request approved successfully")

        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except RequestNotFound as error:
            raise HTTPException(status_code=404, detail=str(error))
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    @router.post(
        "/decline/{request_id}",
        response_model=RequestOutputSchema,
        status_code=200,
    )
    def decline(self, request_id: int):
        user_id = self.payload["sub"]

        try:
            self.service.respond_request(request_id, user_id, False)
            return RequestOutputSchema(msg="Request declined successfully")

        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except RequestNotFound as error:
            raise HTTPException(status_code=404, detail=str(error))
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    @router.get(
        "/all/{project_id}",
        response_model=ListDetailRequestSchema,
        status_code=200,
    )
    def get_all(self, project_id: int):
        user_id = self.payload["sub"]

        try:
            requests = self.service.get_all_requests(project_id, user_id)
            return ListDetailRequestSchema(requests=requests)

        except ProjectNotFound as error:
            raise HTTPException(status_code=404, detail=str(error))
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    @router.get(
        "/{request_id}",
        response_model=DetailRequestSchema,
        status_code=200,
    )
    def get_request(self, request_id: int):
        user_id = self.payload["sub"]

        try:
            request = self.service.get_request(request_id, user_id)
            return request
        except RequestNotFound as error:
            raise HTTPException(status_code=404, detail=str(error))
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))