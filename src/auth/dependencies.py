from fastapi import Depends

from core.security.password_manager import PasswordManager

from users.repositories.user_repository import UserRepository
from users.dependencies import get_user_repository

from .services.auth_services import AuthService

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_manager: PasswordManager = Depends()
):
    return AuthService(user_repo, password_manager)