from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.comun import ErrorResponse
from app.schemas.escenario import (
    EscenarioDetail,
    EscenarioList,
    PaginatedEscenarioResponse,
)
from app.schemas.frase import FraseDetail, FraseList
from app.services.escenario_service import (
    FiltrosEscenario,
    get_escenario,
    get_escenarios,
)

router = APIRouter(prefix="/escenarios", tags=["Escenarios"])


@router.get(
    "",
    response_model=PaginatedEscenarioResponse,
    summary="Listar escenarios",
    responses={
        422: {"model": ErrorResponse, "description": "Error de validacion"},
    },
)
async def listar_escenarios(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre (ILIKE)"),
    pagina: int = Query(1, ge=1, description="Numero de pagina"),
    tamanio: int = Query(20, ge=1, le=100, description="Elementos por pagina"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retorna un listado paginado de escenarios."""
    filters = FiltrosEscenario(
        activo=activo,
        buscar=buscar,
        pagina=pagina,
        tamanio=tamanio,
    )
    escenarios, total_elementos, pagina_actual, total_paginas = await get_escenarios(
        db, filters
    )

    data = [
        EscenarioList(
            id=e.id,
            nombre=e.nombre,
            descripcion=e.descripcion,
            icono=e.icono,
            total_frases=len(e.frases) if e.frases else 0,
            activo=e.activo,
            fecha_creacion=e.fecha_creacion,
        )
        for e in escenarios
    ]
    return PaginatedEscenarioResponse(
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
    response_model=EscenarioDetail,
    summary="Obtener detalle de un escenario con sus frases",
    responses={
        404: {"model": ErrorResponse, "description": "Escenario no encontrado"},
    },
)
async def obtener_escenario(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retorna el detalle completo de un escenario con sus frases asociadas."""
    escenario = await get_escenario(db, id)
    if not escenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escenario no encontrado",
        )
    # Filtrar solo frases activas
    frases_activas = [f for f in (escenario.frases or []) if f.activo]
    return EscenarioDetail(
        id=escenario.id,
        nombre=escenario.nombre,
        descripcion=escenario.descripcion,
        icono=escenario.icono,
        activo=escenario.activo,
        fecha_creacion=escenario.fecha_creacion,
        fecha_actualizacion=escenario.fecha_actualizacion,
        frases=[FraseDetail.model_validate(f) for f in frases_activas],
    )
