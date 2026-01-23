from fastapi import HTTPException, status
from app.domain.abc_repositories.user_repository import IUserRepository
from app.domain.models.user import User
from app.infrastructure.security import get_password_hash, verify_password, create_access_token
from app.application.users.dto import UserRegisterIn, UserLoginIn, Token

class RegisterUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, data: UserRegisterIn) -> dict:
        existing_user = await self.repository.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(data.password)
        new_user = User(email=data.email, password_hash=hashed_password)
        await self.repository.create(new_user)
        return {"message": "User registered successfully"}

class LoginUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, data: UserLoginIn) -> Token:
        user = await self.repository.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")