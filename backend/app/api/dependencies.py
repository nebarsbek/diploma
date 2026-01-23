import jwt #type:ignore 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.configs import settings
from app.infrastructure.database import get_db
from app.infrastructure.orm.user_repository import SqlUserRepository
from app.domain.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)

async def get_current_user(
    token_bearer: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    token_oauth: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    if token_bearer:
        token = token_bearer.credentials
    elif token_oauth:
        token = token_oauth

    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.jwt_settings.JWT_SECRET_KEY,
            algorithms=[settings.jwt_settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    repo = SqlUserRepository(db)
    user = await repo.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_optional(
    token_oauth: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    if not token_oauth:
        return None
    try:
        return await get_current_user(token_bearer=None, token_oauth=token_oauth, db=db)
    except HTTPException:
        return None
