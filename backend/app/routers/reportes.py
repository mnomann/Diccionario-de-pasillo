from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_admin_user, get_current_user
from app.models.usuario import Usuario
from app.schemas.comun import ErrorResponse
from app.schemas.reporte import (
    PaginatedReporteResponse,
    ReporteCreate,
    ReporteDetail,
    ReporteResponse,
    ReporteUpdate,
)
from app.schemas.usuario import UsuarioResponse
from app.services.reporte_service import (
    FiltrosReporte,
    create_reporte,
    get_reporte,
    get_reportes,
    update_reporte,
)

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.post(
    "",
    response_model=ReporteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un reporte",
    responses={
        422: {"model": ErrorResponse, "description": "Error de validacion"},
    },
)
async def crear_reporte(
    data: ReporteCreate,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
) -> Any:
    """Crea un nuevo reporte.

    Requiere autenticacion. El reporte se asocia automaticamente al usuario
    que realiza la denuncia.
    """
    reporte = await create_reporte(
        db, data, usuario_id=usuario.id
    )
    return ReporteResponse(
        id=reporte.id,
        tipo=reporte.tipo,
        entidad_tipo=reporte.entidad_tipo,
        entidad_id=reporte.entidad_id,
        descripcion=reporte.descripcion,
        detalle_contacto=reporte.detalle_contacto,
        estado=reporte.estado,
        fecha_creacion=reporte.fecha_creacion,
    )


@router.get(
    "",
    response_model=PaginatedReporteResponse,
    summary="Listar reportes (solo admin)",
    responses={
        401: {"model": ErrorResponse, "description": "No autenticado"},
        403: {"model": ErrorResponse, "description": "Acceso denegado"},
    },
)
async def listar_reportes(
    pagina: int = Query(1, ge=1, description="Numero de pagina"),
    tamanio: int = Query(20, ge=1, le=100, description="Elementos por pagina"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de reporte"),
    entidad_tipo: Optional[str] = Query(
        None, description="Filtrar por tipo de entidad"
    ),
    db: AsyncSession = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
) -> Any:
    """Retorna la lista de reportes paginados.

    Solo accesible por usuarios administradores.
    Permite filtrar por estado, tipo y entidad_tipo.
    """
    filters = FiltrosReporte(
        pagina=pagina,
        tamanio=tamanio,
        estado=estado,
        tipo=tipo,
        entidad_tipo=entidad_tipo,
    )
    reportes, total_elementos, pagina_actual, total_paginas = await get_reportes(
        db, filters
    )

    data = [
        ReporteDetail(
            id=r.id,
            tipo=r.tipo,
            entidad_tipo=r.entidad_tipo,
            entidad_id=r.entidad_id,
            descripcion=r.descripcion,
            detalle_contacto=r.detalle_contacto,
            estado=r.estado,
            fecha_creacion=r.fecha_creacion,
            usuario=UsuarioResponse.model_validate(r.usuario) if r.usuario else None,
            comentario_admin=r.comentario_admin,
            resuelto_por=r.resuelto_por,
            fecha_actualizacion=r.fecha_actualizacion,
        )
        for r in reportes
    ]

    return PaginatedReporteResponse(
        data=data,
        paginacion={
            "pagina": pagina_actual,
            "tamanio": tamanio,
            "total_elementos": total_elementos,
            "total_paginas": total_paginas,
        },
    )


@router.get(
    "/{reporte_id}",
    response_model=ReporteDetail,
    summary="Obtener detalle de un reporte (solo admin)",
    responses={
        401: {"model": ErrorResponse, "description": "No autenticado"},
        403: {"model": ErrorResponse, "description": "Acceso denegado"},
        404: {"model": ErrorResponse, "description": "Reporte no encontrado"},
    },
)
async def obtener_reporte(
    reporte_id: int,
    db: AsyncSession = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
) -> Any:
    """Retorna el detalle completo de un reporte.

    Solo accesible por usuarios administradores.
    """
    reporte = await get_reporte(db, reporte_id)
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )

    return ReporteDetail(
        id=reporte.id,
        tipo=reporte.tipo,
        entidad_tipo=reporte.entidad_tipo,
        entidad_id=reporte.entidad_id,
        descripcion=reporte.descripcion,
        detalle_contacto=reporte.detalle_contacto,
        estado=reporte.estado,
        fecha_creacion=reporte.fecha_creacion,
        usuario=UsuarioResponse.model_validate(reporte.usuario)
        if reporte.usuario
        else None,
        comentario_admin=reporte.comentario_admin,
        resuelto_por=reporte.resuelto_por,
        fecha_actualizacion=reporte.fecha_actualizacion,
    )


@router.patch(
    "/{reporte_id}",
    response_model=ReporteDetail,
    summary="Actualizar estado y comentario de un reporte (solo admin)",
    responses={
        401: {"model": ErrorResponse, "description": "No autenticado"},
        403: {"model": ErrorResponse, "description": "Acceso denegado"},
        404: {"model": ErrorResponse, "description": "Reporte no encontrado"},
        422: {"model": ErrorResponse, "description": "Error de validacion"},
    },
)
async def actualizar_reporte(
    reporte_id: int,
    data: ReporteUpdate,
    db: AsyncSession = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
) -> Any:
    """Actualiza el estado y/o comentario de un reporte.

    Solo accesible por usuarios administradores.
    Al marcar como 'resuelto' o 'rechazado' se registra automaticamente
    el administrador que realizo la accion.
    """
    reporte = await update_reporte(db, reporte_id, data, admin_id=admin.id)
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )

    return ReporteDetail(
        id=reporte.id,
        tipo=reporte.tipo,
        entidad_tipo=reporte.entidad_tipo,
        entidad_id=reporte.entidad_id,
        descripcion=reporte.descripcion,
        detalle_contacto=reporte.detalle_contacto,
        estado=reporte.estado,
        fecha_creacion=reporte.fecha_creacion,
        usuario=UsuarioResponse.model_validate(reporte.usuario)
        if reporte.usuario
        else None,
        comentario_admin=reporte.comentario_admin,
        resuelto_por=reporte.resuelto_por,
        fecha_actualizacion=reporte.fecha_actualizacion,
    )
