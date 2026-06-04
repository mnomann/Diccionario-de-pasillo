import math
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.palabra import Palabra
from app.schemas.palabra import PalabraCreate, PalabraUpdate
from app.services.comun import aplicar_ordenamiento, aplicar_paginacion


class FiltrosPalabra:
    def __init__(
        self,
        categoria: Optional[str] = None,
        buscar: Optional[str] = None,
        nivel_ironia_min: Optional[float] = None,
        ordenar: str = "fecha_creacion",
        direccion: str = "desc",
        pagina: int = 1,
        tamanio: int = 20,
    ):
        self.categoria = categoria
        self.buscar = buscar
        self.nivel_ironia_min = nivel_ironia_min
        self.ordenar = ordenar
        self.direccion = direccion
        self.pagina = pagina
        self.tamanio = tamanio


async def get_palabras(
    db: AsyncSession,
    filters: FiltrosPalabra,
) -> tuple[list[Palabra], int, int, int]:
    """
    Retorna (palabras, total_elementos, pagina, total_paginas).
    """
    query = select(Palabra).where(Palabra.activo.is_(True))

    if filters.categoria:
        query = query.where(Palabra.categoria == filters.categoria)
    if filters.buscar:
        query = query.where(Palabra.palabra.ilike(f"%{filters.buscar}%"))
    if filters.nivel_ironia_min is not None:
        query = query.where(Palabra.nivel_ironia >= filters.nivel_ironia_min)

    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_elementos: int = total_result.scalar_one()

    query = aplicar_ordenamiento(
        query, Palabra, filters.ordenar, filters.direccion,
        columna_por_defecto="fecha_creacion",
    )
    pagina = filters.pagina
    tamanio = filters.tamanio
    query = aplicar_paginacion(query, pagina, tamanio)

    result = await db.execute(query)
    palabras = list(result.scalars().all())

    total_paginas = max(1, math.ceil(total_elementos / tamanio)) if total_elementos > 0 else 0

    return palabras, total_elementos, pagina, total_paginas


async def get_palabra(db: AsyncSession, palabra_id: int) -> Optional[Palabra]:
    result = await db.execute(
        select(Palabra).where(Palabra.id == palabra_id, Palabra.activo.is_(True))
    )
    return result.scalar_one_or_none()


async def create_palabra(db: AsyncSession, data: PalabraCreate) -> Palabra:
    palabra = Palabra(
        palabra=data.palabra,
        traduccion=data.traduccion,
        categoria=data.categoria,
        nivel_formalidad=data.nivel_formalidad,
        nivel_ironia=data.nivel_ironia,
        nivel_sarcasmo=data.nivel_sarcasmo,
        pronunciacion_fonetica=data.pronunciacion_fonetica,
        ejemplo_uso=data.ejemplo_uso,
        nota_cultural=data.nota_cultural,
        origen=data.origen,
        variantes=data.variantes,
    )
    db.add(palabra)
    await db.flush()
    await db.refresh(palabra)
    return palabra


async def update_palabra(
    db: AsyncSession, palabra_id: int, data: PalabraUpdate
) -> Optional[Palabra]:
    result = await db.execute(
        select(Palabra).where(Palabra.id == palabra_id, Palabra.activo.is_(True))
    )
    palabra = result.scalar_one_or_none()
    if palabra is None:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(palabra, field, value)

    await db.flush()
    await db.refresh(palabra)
    return palabra
