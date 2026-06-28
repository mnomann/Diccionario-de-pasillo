from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.comun import ErrorResponse
from app.schemas.frase import FraseDetail, FraseList, PaginatedFraseResponse
from app.services.frase_service import FiltrosFrase, get_frase, get_frases

router = APIRouter(prefix="/frases", tags=["Frases"])


@router.get(
    "",
    response_model=PaginatedFraseResponse,
    summary="Listar frases",
    responses={
        422: {"model": ErrorResponse, "description": "Error de validacion"},
    },
)
async def listar_frases(
    escenario_id: Optional[int] = Query(None, description="Filtrar por escenario"),
    buscar: Optional[str] = Query(None, description="Buscar por frase original (ILIKE)"),
    tono: Optional[str] = Query(None, description="Filtrar por tono"),
    nivel_formalidad_min: Optional[float] = Query(
        None, ge=0.0, le=10.0, description="Nivel de formalidad minimo"
    ),
    nivel_formalidad_max: Optional[float] = Query(
        None, ge=0.0, le=10.0, description="Nivel de formalidad maximo"
    ),
    pagina: int = Query(1, ge=1, description="Numero de pagina"),
    tamanio: int = Query(20, ge=1, le=100, description="Elementos por pagina"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retorna un listado paginado de frases activas."""
    filters = FiltrosFrase(
        escenario_id=escenario_id,
        buscar=buscar,
        tono=tono,
        nivel_formalidad_min=nivel_formalidad_min,
        nivel_formalidad_max=nivel_formalidad_max,
        pagina=pagina,
        tamanio=tamanio,
    )
    frases, total_elementos, pagina_actual, total_paginas = await get_frases(
        db, filters
    )

    data = [FraseList.model_validate(f) for f in frases]
    return PaginatedFraseResponse(
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
    response_model=FraseDetail,
    summary="Obtener detalle de una frase",
    responses={
        404: {"model": ErrorResponse, "description": "Frase no encontrada"},
    },
)
async def obtener_frase(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Retorna el detalle completo de una frase por su ID."""
    frase = await get_frase(db, id)
    if not frase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frase no encontrada",
        )
    return frase
