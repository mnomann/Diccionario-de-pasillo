from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.usuario import Usuario
from app.services.auth_service import get_current_user

security_scheme = HTTPBearer(auto_error=False)

__all__ = [
    "get_db",
    "get_current_user",
    "get_optional_current_user",
    "get_admin_user",
]


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[Usuario]:
    """Dependency que retorna el usuario autenticado si hay token, o None si no.

    A diferencia de get_current_user, no levanta error si falta el token.
    Util para endpoints que aceptan tanto usuarios autenticados como anonimos.
    """
    if credentials is None:
        return None

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None

    raw_sub = payload.get("sub")
    if raw_sub is None:
        return None
    user_id = int(raw_sub)

    result = await db.execute(select(Usuario).where(Usuario.id == user_id))
    user = result.scalar_one_or_none()
    if user is None or not user.activo:
        return None

    return user


async def get_admin_user(
    usuario: Usuario = Depends(get_current_user),
) -> Usuario:
    """Dependency que extiende get_current_user y verifica que sea administrador.

    Levanta HTTP 403 si el usuario autenticado no es admin.
    """
    if not usuario.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador para acceder a este recurso",
        )
    return usuario
