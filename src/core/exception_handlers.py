from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from project_invitations.exceptions.project_invitation_exceptions import (
    InvitationAlreadyExistsError,
    InvitationNotFoundError,
)
from projects.exceptions.project_exception import (
    ProjectAlreadyHasStatus,
    ProjectInsufficientPrivileges,
    ProjectNotFoundError,
)
from requests.exceptions import (
    CollaboratorAlreadyExists,
    ProjectNotFoundError as ProjectNotFoundRequests,
    RequestAlreadyExists,
    RequestAlreadyRespondedError,
    RequestNotFound,
)


# Handler exceptions rate limit exceeded
def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Handler exceptions for project invitation
def register_invitation_exception_handlers(app):
    @app.exception_handler(PermissionError)
    async def permission_handler(request: Request, exc: PermissionError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(InvitationAlreadyExistsError)
    async def already_exists_handler(
        request: Request, exc: InvitationAlreadyExistsError
    ):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvitationNotFoundError)
    async def not_found_handler(request: Request, exc: InvitationNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})


# Handler exceptions for project
def register_project_exception_handlers(app):
    @app.exception_handler(Exception)
    async def handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    @app.exception_handler(ProjectNotFoundError)
    async def not_found_handler(request: Request, exc: ProjectNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ProjectInsufficientPrivileges)
    async def insufficient_privileges_handler(
        request: Request, exc: ProjectInsufficientPrivileges
    ):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(ProjectAlreadyHasStatus)
    async def already_has_status_handler(
        request: Request, exc: ProjectAlreadyHasStatus
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)})


# Handler exceptions for requests
def register_request_exception_handlers(app):
    @app.exception_handler(Exception)
    async def handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    @app.exception_handler(RequestNotFound)
    async def not_found_handler(request: Request, exc: RequestNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(CollaboratorAlreadyExists)
    async def collaborator_already_exists_handler(
        request: Request, exc: CollaboratorAlreadyExists
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(ProjectNotFoundRequests)
    async def project_not_found_handler(request: Request, exc: ProjectNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(RequestAlreadyExists)
    async def request_already_exists_handler(request: Request, exc: RequestAlreadyExists):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(RequestAlreadyRespondedError)
    async def request_already_responded_handler(request: Request, exc: RequestAlreadyRespondedError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})