import math
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.frase import Frase
from app.schemas.frase import FraseCreate
from app.services.comun import aplicar_ordenamiento, aplicar_paginacion


class FiltrosFrase:
    def __init__(
        self,
        escenario_id: Optional[int] = None,
        buscar: Optional[str] = None,
        tono: Optional[str] = None,
        nivel_formalidad_min: Optional[float] = None,
        nivel_formalidad_max: Optional[float] = None,
        pagina: int = 1,
        tamanio: int = 20,
    ):
        self.escenario_id = escenario_id
        self.buscar = buscar
        self.tono = tono
        self.nivel_formalidad_min = nivel_formalidad_min
        self.nivel_formalidad_max = nivel_formalidad_max
        self.pagina = pagina
        self.tamanio = tamanio


async def get_frases(
    db: AsyncSession,
    filters: FiltrosFrase,
) -> tuple[list[Frase], int, int, int]:
    query = (
        select(Frase)
        .options(selectinload(Frase.escenario))
        .where(Frase.activo.is_(True))
    )

    if filters.escenario_id is not None:
        query = query.where(Frase.escenario_id == filters.escenario_id)
    if filters.buscar:
        query = query.where(Frase.frase_original.ilike(f"%{filters.buscar}%"))
    if filters.tono:
        query = query.where(Frase.tono == filters.tono)
    if filters.nivel_formalidad_min is not None:
        query = query.where(Frase.nivel_formalidad >= filters.nivel_formalidad_min)
    if filters.nivel_formalidad_max is not None:
        query = query.where(Frase.nivel_formalidad <= filters.nivel_formalidad_max)

    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_elementos: int = total_result.scalar_one()

    query = aplicar_ordenamiento(
        query, Frase, "fecha_creacion", "desc",
        columna_por_defecto="fecha_creacion",
    )
    pagina = filters.pagina
    tamanio = filters.tamanio
    query = aplicar_paginacion(query, pagina, tamanio)

    result = await db.execute(query)
    frases = list(result.scalars().all())

    total_paginas = max(1, math.ceil(total_elementos / tamanio)) if total_elementos > 0 else 0

    return frases, total_elementos, pagina, total_paginas


async def get_frase(db: AsyncSession, frase_id: int) -> Optional[Frase]:
    result = await db.execute(
        select(Frase)
        .options(selectinload(Frase.escenario))
        .where(Frase.id == frase_id, Frase.activo.is_(True))
    )
    return result.scalar_one_or_none()


async def create_frase(db: AsyncSession, data: FraseCreate) -> Frase:
    frase = Frase(
        escenario_id=data.escenario_id,
        frase_original=data.frase_original,
        traduccion=data.traduccion,
        explicacion=data.explicacion,
        tono=data.tono,
        intencion_real=data.intencion_real,
        nivel_formalidad=data.nivel_formalidad,
        nivel_ironia=data.nivel_ironia,
        nivel_sarcasmo=data.nivel_sarcasmo,
        ejemplo_uso=data.ejemplo_uso,
    )
    db.add(frase)
    await db.flush()
    await db.refresh(frase)
    # Cargar relacion escenario
    await db.refresh(frase, attribute_names=["escenario"])
    return frase
