from core.security.password_manager import PasswordManager

from users.repositories.user_repository import UserRepository
from users.models.user import User

from ..exceptions.auth_exception import InvalidCredentialsException
from ..schemas.auth_schema import RegisterInputSchema, LoginInputSchema, UserCreateSchema


class AuthService:

    def __init__(
            self, 
            user_repo: UserRepository, 
            password_manager: PasswordManager
        ):
        self.user_repo = user_repo
        self.password_manager = password_manager

    def _get_user_by_email_or_raise(self, email: str):
        user = self.user_repo.get_user_by_email(email)        
        return user

    def register_user(self, data: RegisterInputSchema):
        if self._get_user_by_email_or_raise(data.email):
            raise Exception("Email already assigned to user")

        hashed_password = self.password_manager.hash(data.password)

        user_create = UserCreateSchema(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            bio=data.bio,
            email=data.email,
            password=hashed_password
        )

        user_entity = User(**user_create.model_dump())
        return self.user_repo.create(user_entity)

    def authenticate(self, data: LoginInputSchema):
        user = self._get_user_by_email_or_raise(data.email)
        if not user:
            raise InvalidCredentialsException("Invalid credentials")
        
        if not self.password_manager.verify(data.password, user.password):
            raise InvalidCredentialsException("Invalid credentials")

        return user.id