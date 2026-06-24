from uvicorn import run
from fastapi import FastAPI

from users.controllers.user_controller import router as user_router
from auth.controllers.auth_controller import router as auth_router
from projects.controllers.project_controller import router as project_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)

if __name__ == "__main__":
    run(app)