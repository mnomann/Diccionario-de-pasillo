import math
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reporte import Reporte
from app.schemas.reporte import ReporteCreate, ReporteUpdate
from app.services.comun import aplicar_ordenamiento, aplicar_paginacion


class FiltrosReporte:
    """Filtros para la consulta de reportes."""

    def __init__(
        self,
        pagina: int = 1,
        tamanio: int = 20,
        estado: Optional[str] = None,
        tipo: Optional[str] = None,
        entidad_tipo: Optional[str] = None,
    ):
        self.pagina = pagina
        self.tamanio = tamanio
        self.estado = estado
        self.tipo = tipo
        self.entidad_tipo = entidad_tipo


async def create_reporte(
    db: AsyncSession,
    data: ReporteCreate,
    usuario_id: Optional[int] = None,
) -> Reporte:
    """Crea un nuevo reporte asociado al usuario autenticado.

    El usuario_id es obligatorio (viene del token JWT).
    El detalle_contacto ya no se solicita en el formulario porque el
    usuario queda identificado por su cuenta.
    """
    reporte = Reporte(
        tipo=data.tipo,
        entidad_tipo=data.entidad_tipo,
        entidad_id=data.entidad_id,
        descripcion=data.descripcion,
        detalle_contacto=None,
        usuario_id=usuario_id,
        estado="pendiente",
    )
    db.add(reporte)
    await db.flush()
    await db.refresh(reporte)
    return reporte


async def get_reportes(
    db: AsyncSession,
    filters: FiltrosReporte,
) -> tuple[list[Reporte], int, int, int]:
    """Retorna reportes paginados con filtros opcionales.

    Returns:
        tuple: (reportes, total_elementos, pagina_actual, total_paginas)
    """
    query = select(Reporte)

    # Aplicar filtros
    if filters.estado:
        query = query.where(Reporte.estado == filters.estado)
    if filters.tipo:
        query = query.where(Reporte.tipo == filters.tipo)
    if filters.entidad_tipo:
        query = query.where(Reporte.entidad_tipo == filters.entidad_tipo)

    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_elementos: int = total_result.scalar_one()

    query = aplicar_ordenamiento(
        query,
        Reporte,
        "fecha_creacion",
        "desc",
        columna_por_defecto="fecha_creacion",
    )
    query = aplicar_paginacion(query, filters.pagina, filters.tamanio)

    result = await db.execute(query)
    reportes = list(result.scalars().all())

    total_paginas = (
        max(1, math.ceil(total_elementos / filters.tamanio))
        if total_elementos > 0
        else 0
    )

    return reportes, total_elementos, filters.pagina, total_paginas


async def get_reporte(
    db: AsyncSession,
    reporte_id: int,
) -> Optional[Reporte]:
    """Obtiene un reporte por su ID."""
    result = await db.execute(select(Reporte).where(Reporte.id == reporte_id))
    return result.scalar_one_or_none()


async def update_reporte(
    db: AsyncSession,
    reporte_id: int,
    data: ReporteUpdate,
    admin_id: int,
) -> Optional[Reporte]:
    """Actualiza el estado y/o comentario de un reporte.

    Si se cambia a un estado final (resuelto, rechazado),
    se registra quien lo resolvio.
    """
    result = await db.execute(select(Reporte).where(Reporte.id == reporte_id))
    reporte = result.scalar_one_or_none()
    if not reporte:
        return None

    if data.estado is not None:
        reporte.estado = data.estado
        # Registrar quien resolvio cuando se marca como resuelto o rechazado
        if data.estado in ("resuelto", "rechazado"):
            reporte.resuelto_por = admin_id

    if data.comentario_admin is not None:
        reporte.comentario_admin = data.comentario_admin

    reporte.fecha_actualizacion = func.now()
    await db.flush()
    await db.refresh(reporte)
    return reporte
