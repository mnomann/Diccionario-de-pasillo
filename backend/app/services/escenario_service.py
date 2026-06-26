import math
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.escenario import Escenario
from app.schemas.escenario import EscenarioCreate
from app.services.comun import aplicar_ordenamiento, aplicar_paginacion


class FiltrosEscenario:
    def __init__(
        self,
        activo: Optional[bool] = None,
        buscar: Optional[str] = None,
        pagina: int = 1,
        tamanio: int = 20,
    ):
        self.activo = activo
        self.buscar = buscar
        self.pagina = pagina
        self.tamanio = tamanio


async def get_escenarios(
    db: AsyncSession,
    filters: FiltrosEscenario,
) -> tuple[list[Escenario], int, int, int]:
    query = select(Escenario).options(selectinload(Escenario.frases))

    if filters.activo is not None:
        query = query.where(Escenario.activo.is_(filters.activo))
    else:
        query = query.where(Escenario.activo.is_(True))
    if filters.buscar:
        query = query.where(Escenario.nombre.ilike(f"%{filters.buscar}%"))

    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_elementos: int = total_result.scalar_one()

    query = aplicar_ordenamiento(
        query, Escenario, "nombre", "asc",
        columna_por_defecto="nombre",
    )
    pagina = filters.pagina
    tamanio = filters.tamanio
    query = aplicar_paginacion(query, pagina, tamanio)

    result = await db.execute(query)
    escenarios = list(result.scalars().all())

    total_paginas = max(1, math.ceil(total_elementos / tamanio)) if total_elementos > 0 else 0

    return escenarios, total_elementos, pagina, total_paginas


async def get_escenario(db: AsyncSession, escenario_id: int) -> Optional[Escenario]:
    result = await db.execute(
        select(Escenario)
        .options(selectinload(Escenario.frases))
        .where(Escenario.id == escenario_id)
    )
    escenario = result.scalar_one_or_none()
    return escenario


async def create_escenario(db: AsyncSession, data: EscenarioCreate) -> Escenario:
    escenario = Escenario(
        nombre=data.nombre,
        descripcion=data.descripcion,
        icono=data.icono,
    )
    db.add(escenario)
    await db.flush()
    await db.refresh(escenario)
    return escenario
