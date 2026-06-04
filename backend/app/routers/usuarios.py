from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.sugerencia import Sugerencia
from app.models.usuario import Usuario
from app.schemas.comun import ErrorResponse
from app.schemas.usuario import UsuarioMe
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get(
    "/me",
    response_model=UsuarioMe,
    summary="Obtener perfil del usuario autenticado",
    responses={
        401: {"model": ErrorResponse, "description": "No autenticado"},
    },
)
async def obtener_perfil(
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
) -> Any:
    """Retorna el perfil del usuario autenticado con estadisticas."""
    # Contar sugerencias del usuario
    count_result = await db.execute(
        select(func.count()).select_from(
            select(Sugerencia).where(Sugerencia.usuario_id == usuario.id).subquery()
        )
    )
    total_sugerencias: int = count_result.scalar_one()

    # Contar sugerencias por estado
    estado_result = await db.execute(
        select(Sugerencia.estado, func.count().label("cantidad"))
        .where(Sugerencia.usuario_id == usuario.id)
        .group_by(Sugerencia.estado)
    )
    sugerencias_por_estado = {
        row.estado: row.cantidad for row in estado_result.all()
    }

    estadisticas = {
        "total_sugerencias": total_sugerencias,
        "sugerencias_por_estado": sugerencias_por_estado,
    }

    return UsuarioMe(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        fecha_registro=usuario.fecha_registro,
        preferencias=usuario.preferencias,
        ultima_conexion=usuario.ultima_conexion,
        estadisticas=estadisticas,
    )
