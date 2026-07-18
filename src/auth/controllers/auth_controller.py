from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_restful.cbv import cbv

from core.security.jwt_manager import JwtManager, jwt_required

from ..dependencies import get_auth_service
from ..exceptions.auth_exception import InvalidCredentialsException
from ..schemas.auth_schema import (
    LoginInputSchema,
    LoginOutputSchema,
    LogoutOutputSchema,
    RegisterInputSchema,
    RegisterOutputSchema,
)
from ..services.auth_services import AuthService

router = APIRouter(prefix="/auth/api/v1", tags=["auth"])


@cbv(router)
class AuthController:
    service: AuthService = Depends(get_auth_service)
    payload: dict = Depends(jwt_required)

    @router.post(
        "/register",
        response_model=RegisterOutputSchema,
        status_code=201,
    )
    def register(
        self,
        data: RegisterInputSchema,
    ):
        self.service.register_user(data)

        return RegisterOutputSchema(msg="Register successfully")

    @router.post(
        "/login",
        response_model=LoginOutputSchema,
        status_code=200,
    )
    def login(
        self,
        data: LoginInputSchema,
        response: Response,
        jwt_manager: JwtManager = Depends(),
    ):
        try:
            user_id = self.service.authenticate(data)

            access_token = jwt_manager.create_access_token(user_id=user_id)
            refresh_token = jwt_manager.create_refresh_token(user_id=user_id)

            response.set_cookie(key="access_token", value=access_token)
            response.set_cookie(key="refresh_token", value=refresh_token)

            return {"access_token": access_token, "refresh_token": refresh_token}

        except InvalidCredentialsException:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    @router.post("/logout", response_model=LogoutOutputSchema, status_code=200)
    def logout(
        self,
        response: Response,
    ):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return LogoutOutputSchema(msg="Logout successfully")

    @router.get(
        "/refresh",
        response_model=LoginOutputSchema,
        status_code=200,
    )
    def refresh(self, response: Response):
        user_id = self.payload["sub"]

        access_token = JwtManager.create_access_token(user_id=user_id)
        refresh_token = JwtManager.create_refresh_token(user_id=user_id)

        response.set_cookie(key="access_token", value=access_token)
        response.set_cookie(key="refresh_token", value=refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}
