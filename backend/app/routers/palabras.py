from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.comun import ErrorResponse
from app.schemas.palabra import (
    PaginatedPalabraResponse,
    PalabraDetail,
    PalabraList,
)
from app.services.palabra_service import FiltrosPalabra, get_palabra, get_palabras

router = APIRouter(prefix="/palabras", tags=["Palabras"])


@router.get(
    "",
    response_model=PaginatedPalabraResponse,
    summary="Listar palabras",
    responses={
        422: {"model": ErrorResponse, "description": "Error de validacion"},
    },
)
async def listar_palabras(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    buscar: Optional[str] = Query(None, description="Buscar por palabra (ILIKE)"),
    nivel_ironia_min: Optional[float] = Query(
        None, ge=0.0, le=10.0, description="Nivel de ironia minimo"
    ),
    ordenar: str = Query("fecha_creacion", description="Campo de ordenamiento"),
    direccion: str = Query("desc", description="Direccion: asc o desc"),
    pagina: int = Query(1, ge=1, description="Numero de pagina"),
    tamanio: int = Query(20, ge=1, le=100, description="Elementos por pagina"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retorna un listado paginado de palabras activas."""
    filters = FiltrosPalabra(
        categoria=categoria,
        buscar=buscar,
        nivel_ironia_min=nivel_ironia_min,
        ordenar=ordenar,
        direccion=direccion,
        pagina=pagina,
        tamanio=tamanio,
    )
    palabras, total_elementos, pagina_actual, total_paginas = await get_palabras(
        db, filters
    )

    data = [PalabraList.model_validate(p) for p in palabras]
    return PaginatedPalabraResponse(
        data=data,
        paginacion={
            "pagina": pagina_actual,
            "tamanio": tamanio,
            "total_elementos": total_elementos,
            "total_paginas": total_paginas,
        },
    )


@router.get(
    "/{id}",
    response_model=PalabraDetail,
    summary="Obtener detalle de una palabra",
    responses={
        404: {"model": ErrorResponse, "description": "Palabra no encontrada"},
    },
)
async def obtener_palabra(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retorna el detalle completo de una palabra por su ID."""
    palabra = await get_palabra(db, id)
    if not palabra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palabra no encontrada",
        )
    return palabra
