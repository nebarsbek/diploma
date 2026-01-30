from pydantic import BaseModel
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.infrastructure.database import get_db
from app.infrastructure.orm.user_repository import SqlUserRepository
from app.application.users.use_cases import LoginUserUseCase
from app.application.users.dto import UserRegisterIn, UserLoginIn, Token, UserRegisterOut
from app.domain.models.user import User
from app.api.dependencies import get_current_user_optional, get_current_user
from app.core.configs import settings
from app.core.email import send_verification_email, send_reset_password_email
from app.infrastructure.security import get_password_hash, verify_password
from jose import jwt, JWTError # type: ignore

router = APIRouter()

class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class UserForgotPasswordIn(BaseModel):
    email: str

class UserResetPasswordIn(BaseModel):
    token: str
    new_password: str

def get_login_use_case(db=Depends(get_db)) -> LoginUserUseCase:
    return LoginUserUseCase(SqlUserRepository(db))

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}

@router.post("/create-user", response_model=UserRegisterOut)
async def create_user(
    data: UserRegisterIn,
    db = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    Создание пользователя (Сотрудника).
    Если в базе нет пользователей, первый создается как admin.
    Иначе требуется роль admin.
    """
    repo = SqlUserRepository(db)
    user_count = await repo.count()
    
    role = "employee"
    if user_count == 0:
        role = "admin"
    else:
        if not current_user or current_user.role != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    existing_user = await repo.get_by_email(data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(data.password)
    user = User(email=data.email, password_hash=hashed_password, role=role)
    created_user = await repo.create(user)
    return UserRegisterOut(id=created_user.id, email=created_user.email)

@router.post("/register")
async def register(
    data: UserRegisterIn,
    db = Depends(get_db)
):
    repo = SqlUserRepository(db)
    existing_user = await repo.get_by_email(data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(data.password)
    
    # Создаем токен, содержащий все данные для регистрации
    payload = {
        "sub": data.email,
        "password_hash": hashed_password,
        "role": "customer",
        "type": "registration"
    }
    token = jwt.encode(payload, settings.jwt_settings.JWT_SECRET_KEY, algorithm=settings.jwt_settings.JWT_ALGORITHM)
    logger.info(f"Generated token: {token}")
    logger.info(f"Email: {data.email}")
    logger.info(f"Password hash: {hashed_password}")
    
    try:
        await send_verification_email(data.email, token)
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        # Игнорируем ошибку отправки в dev-режиме, чтобы не ломать флоу регистрации
    
    return {"message": "Verification email sent"}

@router.post("/verify-email")
async def verify_email(token: str, db = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_settings.JWT_SECRET_KEY, algorithms=[settings.jwt_settings.JWT_ALGORITHM])
        email = payload.get("sub")
        password_hash = payload.get("password_hash")
        role = payload.get("role")
        
        if not email or not password_hash:
            raise HTTPException(status_code=400, detail="Invalid token")
            
        repo = SqlUserRepository(db)
        if await repo.get_by_email(email):
            return {"message": "User already registered"}
            
        # Создаем пользователя только сейчас
        user = User(email=email, password_hash=password_hash, role=role, is_verified=True)
        await repo.create(user)
        return {"message": "Email verified and user created"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

@router.post("/change-password")
async def change_password(
    data: UserPasswordUpdate,
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.password_hash = get_password_hash(data.new_password)
    
    repo = SqlUserRepository(db)
    await repo.update(current_user)
    
    return {"message": "Password updated successfully"}

@router.post("/forgot-password")
async def forgot_password(
    data: UserForgotPasswordIn,
    db = Depends(get_db)
):
    repo = SqlUserRepository(db)
    user = await repo.get_by_email(data.email)
    if not user:
        # Не сообщаем, что пользователя нет, для безопасности, или возвращаем 404
        raise HTTPException(status_code=404, detail="User not found")

    payload = {
        "sub": user.email,
        "type": "reset_password"
    }
    token = jwt.encode(payload, settings.jwt_settings.JWT_SECRET_KEY, algorithm=settings.jwt_settings.JWT_ALGORITHM)
    
    try:
        await send_reset_password_email(user.email, token)
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        logger.info(f"Reset token for {user.email}: {token}")
        
    return {"message": "Password reset email sent"}

@router.post("/reset-password")
async def reset_password(
    data: UserResetPasswordIn,
    db = Depends(get_db)
):
    try:
        payload = jwt.decode(data.token, settings.jwt_settings.JWT_SECRET_KEY, algorithms=[settings.jwt_settings.JWT_ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        
        if not email or token_type != "reset_password":
             raise HTTPException(status_code=400, detail="Invalid token")
             
        repo = SqlUserRepository(db)
        user = await repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user.password_hash = get_password_hash(data.new_password)
        await repo.update(user)
        
        return {"message": "Password reset successfully"}
        
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

@router.post("/login", response_model=Token)
async def login(
    data: UserLoginIn,
    uc: LoginUserUseCase = Depends(get_login_use_case)
):
    """
    Аутентификация пользователя (получение токена).

    Принимает email и пароль. Возвращает JWT токен доступа (access token).
    """
    return await uc.execute(data)

@router.post("/token", response_model=Token)
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uc: LoginUserUseCase = Depends(get_login_use_case)
):
    """
    Эндпоинт для авторизации через кнопку 'Authorize' в Swagger UI.

    Использует стандарт OAuth2PasswordRequestForm (form-data) для передачи учетных данных.
    """
    # Swagger отправляет username и password. Мы используем email как username.
    return await uc.execute(UserLoginIn(email=form_data.username, password=form_data.password))