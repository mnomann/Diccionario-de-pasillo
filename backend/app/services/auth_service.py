import datetime
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """Genera el hash bcrypt de una contrasena."""
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica una contrasena contra su hash."""
    return pwd_context.verify(password, password_hash)


def create_access_token(data: dict[str, Any]) -> tuple[str, int]:
    """Crea un token JWT. Retorna (token, expires_in_segundos)."""
    to_encode = data.copy()
    expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire_seconds = expire_minutes * 60
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=expire_minutes
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, expire_seconds


def decode_access_token(token: str) -> dict[str, Any]:
    """Decodifica y valida un token JWT. Retorna el payload."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    """Dependency que valida el JWT y retorna el usuario autenticado."""
    payload = decode_access_token(credentials.credentials)
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido: sin identificador de usuario",
        )

    result = await db.execute(select(Usuario).where(Usuario.id == user_id))
    user = result.scalar_one_or_none()
    if user is None or not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
        )
    return user
