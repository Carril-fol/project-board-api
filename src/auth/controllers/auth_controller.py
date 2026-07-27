from fastapi import APIRouter, Depends, HTTPException, Request, Response

from core.security.jwt_manager import JwtManager, jwt_required
from shared.extensions import limiter

from ..dependencies import get_auth_service
from ..exceptions.auth_exception import InvalidCredentialsException
from ..schemas.auth_schema import (
    AuthOutputSchema,
    LoginInputSchema,
    LoginOutputSchema,
    RegisterInputSchema,
)
from ..services.auth_services import AuthService

router = APIRouter(prefix="/auth/api/v1", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthOutputSchema,
    status_code=201,
)
@limiter.limit("5/minute")
def register(
    request: Request,
    data: RegisterInputSchema,
    service: AuthService = Depends(get_auth_service),
):
    service.register_user(data)
    return AuthOutputSchema(msg="Register successfully")


@router.post(
    "/login",
    response_model=LoginOutputSchema,
    status_code=200,
)
@limiter.limit("5/minute")
def login(
    request: Request,
    data: LoginInputSchema,
    response: Response,
    service: AuthService = Depends(get_auth_service),
    jwt_manager: JwtManager = Depends(),
):
    try:
        user_id = service.authenticate(data)

        access_token = jwt_manager.create_access_token(user_id=user_id)
        refresh_token = jwt_manager.create_refresh_token(user_id=user_id)
        response.set_cookie(key="access_token", value=access_token)
        response.set_cookie(key="refresh_token", value=refresh_token)
        return LoginOutputSchema(access_token=access_token, refresh_token=refresh_token)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout", response_model=AuthOutputSchema, status_code=200)
def logout(response: Response, payload: dict = Depends(jwt_required)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return AuthOutputSchema(msg="Logout successfully")


@router.get(
    "/refresh",
    response_model=LoginOutputSchema,
    status_code=200,
)
def refresh(
    response: Response,
    payload: dict = Depends(jwt_required),
):
    user_id = payload["sub"]
    access_token = JwtManager.create_access_token(user_id=user_id)
    refresh_token = JwtManager.create_refresh_token(user_id=user_id)

    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)
    return LoginOutputSchema(access_token=access_token, refresh_token=refresh_token)
