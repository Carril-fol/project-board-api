from fastapi import APIRouter, HTTPException, Response, Depends

from core.security.password_manager import PasswordManager
from core.security.jwt_manager import JwtManager, jwt_required

from users.dependencies import get_user_repository
from users.repositories.user_repository import UserRepository

from ..dependencies import get_auth_service
from ..exceptions.auth_exception import InvalidCredentialsException
from ..schemas.auth_schema import RegisterInputSchema, RegisterOutputSchema, LoginOutputSchema, LoginInputSchema, LogoutOutputSchema
from ..services.auth_services import AuthService


router = APIRouter(prefix="/auth/api/v1", tags=["auth"])

password_manager = PasswordManager()
user_repo: UserRepository = Depends(get_user_repository)
auth_service = AuthService(user_repo, password_manager)


@router.post(
        "/register", 
        response_model=RegisterOutputSchema, 
        status_code=201
    )
async def register(
    data: RegisterInputSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.register_user(data)

    return RegisterOutputSchema(
        msg="Register successfully"
    )


@router.post(
        "/login", 
        response_model=LoginOutputSchema, 
        status_code=200
    )
async def login(
    data: LoginInputSchema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    jwt_manager: JwtManager = Depends(),
):
    try:
        user_id = auth_service.authenticate(data)        

        access_token = jwt_manager.create_access_token(user_id=user_id)
        refresh_token = jwt_manager.create_refresh_token(user_id=user_id)

        response.set_cookie(key="access_token", value=access_token)
        response.set_cookie(key="refresh_token", value=refresh_token)

        return {
            "access_token": access_token, 
            "refresh_token": refresh_token
        }
    
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


@router.post(
        "/logout", 
        response_model=LogoutOutputSchema, 
        status_code=200
    )
async def logout(
    response: Response,
    payload: dict = Depends(jwt_required)
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return LogoutOutputSchema(
        msg="Logout successfully"
    )