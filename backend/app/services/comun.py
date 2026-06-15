import math
from typing import Any, Optional

from sqlalchemy import Select, asc, desc
from sqlalchemy.orm import DeclarativeBase


def aplicar_ordenamiento(
    query: Select,
    model: type[DeclarativeBase],
    ordenar: str,
    direccion: str = "desc",
    columna_por_defecto: str = "fecha_creacion",
) -> Select:
    """Aplica ordenamiento a una consulta SQLAlchemy."""
    columna = ordenar if ordenar else columna_por_defecto
    if not hasattr(model, columna):
        columna = columna_por_defecto

    sort_column = getattr(model, columna)
    if direccion.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    return query


def aplicar_paginacion(query: Select, pagina: int = 1, tamanio: int = 20) -> Select:
    """Aplica paginacion LIMIT/OFFSET a una consulta."""
    offset = (pagina - 1) * tamanio
    return query.offset(offset).limit(tamanio)
