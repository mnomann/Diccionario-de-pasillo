from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.comun import ErrorResponse
from app.schemas.sugerencia import (
    PaginatedSugerenciaResponse,
    SugerenciaCreate,
    SugerenciaList,
    SugerenciaResponse,
)
from app.services.auth_service import get_current_user
from app.services.sugerencia_service import (
    FiltrosSugerencia,
    create_sugerencia,
    get_sugerencias,
)

router = APIRouter(prefix="/sugerencias", tags=["Sugerencias"])


def _resumir_contenido(contenido: dict) -> str:
    """Genera un resumen legible del contenido de una sugerencia."""
    tipo = contenido.get("tipo", "general")
    if tipo == "nueva_palabra":
        palabra = contenido.get("palabra", "")
        return f"Sugerencia de nueva palabra: '{palabra}'"
    elif tipo == "correccion":
        ref = contenido.get("referencia", "")
        return f"Correccion sobre: {ref}"
    elif tipo == "otro":
        mensaje = contenido.get("mensaje", "")
        return f"Consulta general: {mensaje[:100]}"
    return "Sugerencia general"


@router.post(
    "",
    response_model=SugerenciaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar una sugerencia",
    responses={
        401: {"model": ErrorResponse, "description": "No autenticado"},
        422: {"model": ErrorResponse, "description": "Error de validacion"},
    },
)
async def enviar_sugerencia(
    data: SugerenciaCreate,
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
) -> Any:
    """Crea una nueva sugerencia. Requiere autenticacion."""
    sugerencia = await create_sugerencia(
        db, data, usuario_id=usuario.id
    )
    return SugerenciaResponse(
        id=sugerencia.id,
        tipo=sugerencia.tipo,
        estado=sugerencia.estado,
        mensaje="Sugerencia recibida correctamente",
        fecha_creacion=sugerencia.fecha_creacion,
    )


@router.get(
    "",
    response_model=PaginatedSugerenciaResponse,
    summary="Listar sugerencias del usuario autenticado",
    responses={
        401: {"model": ErrorResponse, "description": "No autenticado"},
    },
)
async def listar_sugerencias(
    pagina: int = Query(1, ge=1, description="Numero de pagina"),
    tamanio: int = Query(20, ge=1, le=100, description="Elementos por pagina"),
    db: AsyncSession = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
) -> Any:
    """Retorna las sugerencias del usuario autenticado."""
    filters = FiltrosSugerencia(pagina=pagina, tamanio=tamanio)
    sugerencias, total_elementos, pagina_actual, total_paginas = await get_sugerencias(
        db, usuario.id, filters
    )

    data = [
        SugerenciaList(
            id=s.id,
            tipo=s.tipo,
            contenido_resumen=_resumir_contenido(s.contenido),
            estado=s.estado,
            comentario_moderador=s.comentario_moderador,
            fecha_creacion=s.fecha_creacion,
        )
        for s in sugerencias
    ]
    return PaginatedSugerenciaResponse(
        data=data,
        paginacion={
            "pagina": pagina_actual,
            "tamanio": tamanio,
            "total_elementos": total_elementos,
            "total_paginas": total_paginas,
        },
    )
