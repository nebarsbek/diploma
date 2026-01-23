from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.infrastructure.database import get_db
from app.infrastructure.orm.user_repository import SqlUserRepository
from app.application.users.use_cases import LoginUserUseCase
from app.application.users.dto import UserRegisterIn, UserLoginIn, Token, UserRegisterOut
from app.domain.models.user import User
from app.api.dependencies import get_current_user_optional, get_current_user
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    hashed_password = pwd_context.hash(data.password)
    user = User(email=data.email, password_hash=hashed_password, role=role)
    created_user = await repo.create(user)
    return UserRegisterOut(id=created_user.id, email=created_user.email)

@router.post("/register", response_model=UserRegisterOut)
async def register(
    data: UserRegisterIn,
    db = Depends(get_db)
):
    repo = SqlUserRepository(db)
    existing_user = await repo.get_by_email(data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(data.password)
    user = User(email=data.email, password_hash=hashed_password, role="customer")
    created_user = await repo.create(user)
    return UserRegisterOut(id=created_user.id, email=created_user.email)

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