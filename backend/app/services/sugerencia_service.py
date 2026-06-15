import math
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sugerencia import Sugerencia
from app.schemas.sugerencia import SugerenciaCreate
from app.services.comun import aplicar_ordenamiento, aplicar_paginacion


class FiltrosSugerencia:
    def __init__(
        self,
        pagina: int = 1,
        tamanio: int = 20,
    ):
        self.pagina = pagina
        self.tamanio = tamanio


async def create_sugerencia(
    db: AsyncSession,
    data: SugerenciaCreate,
    usuario_id: Optional[int] = None,
) -> Sugerencia:
    sugerencia = Sugerencia(
        usuario_id=usuario_id,
        tipo=data.tipo,
        contenido=data.contenido,
        usuario_email=data.usuario_email,
        estado="pendiente",
    )
    db.add(sugerencia)
    await db.flush()
    await db.refresh(sugerencia)
    return sugerencia


async def get_sugerencias(
    db: AsyncSession,
    usuario_id: int,
    filters: FiltrosSugerencia,
) -> tuple[list[Sugerencia], int, int, int]:
    query = select(Sugerencia).where(Sugerencia.usuario_id == usuario_id)

    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_elementos: int = total_result.scalar_one()

    query = aplicar_ordenamiento(
        query, Sugerencia, "fecha_creacion", "desc",
        columna_por_defecto="fecha_creacion",
    )
    query = aplicar_paginacion(query, filters.pagina, filters.tamanio)

    result = await db.execute(query)
    sugerencias = list(result.scalars().all())

    total_paginas = max(1, math.ceil(total_elementos / filters.tamanio)) if total_elementos > 0 else 0

    return sugerencias, total_elementos, filters.pagina, total_paginas
