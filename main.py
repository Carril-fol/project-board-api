from fastapi import FastAPI
from uvicorn import run

from auth.controllers.auth_controller import router as auth_router
from collaborators.controllers.collaborators_controller import (
    router as collaborators_router,
)
from project_invitations.controllers.project_invitation_controller import (
    router as project_invitation_router,
)
from projects.controllers.project_controller import router as project_router
from projects_tags.controllers.project_tag_controller import (
    router as project_tag_router,
)
from requests.controllers.requests_controller import router as requests_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(project_tag_router)
app.include_router(collaborators_router)
app.include_router(project_invitation_router)
app.include_router(requests_router)


if __name__ == "__main__":
    run(app)
