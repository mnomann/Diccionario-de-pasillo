import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    LoginRequest,
    LoginResponse,
    UsuarioCreate,
    UsuarioResponse,
)
from app.services.auth_service import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post(
    "/registro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
)
async def registro(
    data: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Registra un nuevo usuario en la plataforma."""
    # Verificar si el email ya existe
    result = await db.execute(
        select(Usuario).where(Usuario.email == data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya esta registrado",
        )

    usuario = Usuario(
        nombre=data.nombre,
        email=data.email,
        contrasena_hash=hash_password(data.contrasena),
        preferencias=data.preferencias or {},
    )
    db.add(usuario)
    await db.flush()
    await db.refresh(usuario)

    return usuario


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesion",
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Autentica un usuario y retorna un token JWT."""
    result = await db.execute(
        select(Usuario).where(Usuario.email == data.email, Usuario.activo.is_(True))
    )
    usuario = result.scalar_one_or_none()

    if not usuario or not verify_password(data.contrasena, usuario.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    # Actualizar ultima conexion
    usuario.ultima_conexion = datetime.datetime.now(datetime.timezone.utc)
    await db.flush()

    token, expires_in = create_access_token({"sub": str(usuario.id)})  # str para compatibilidad con python-jose

    return LoginResponse(
        token=token,
        token_type="bearer",
        expira_en=expires_in,
        usuario=UsuarioResponse.model_validate(usuario),
    )
