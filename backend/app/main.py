from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine
from app.routers import (
    auth_router,
    escenarios_router,
    frases_router,
    palabras_router,
    sugerencias_router,
    usuarios_router,
)
from app.schemas.comun import ErrorResponse

app = FastAPI(
    title="Desenreda API",
    description="API de la plataforma Desenreda - Modismos chilenos para neurodivergentes",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(palabras_router, prefix=API_PREFIX)
app.include_router(frases_router, prefix=API_PREFIX)
app.include_router(escenarios_router, prefix=API_PREFIX)
app.include_router(sugerencias_router, prefix=API_PREFIX)
app.include_router(usuarios_router, prefix=API_PREFIX)


# ---------------------------------------------------------------------------
# Manejadores de errores globales
# ---------------------------------------------------------------------------
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            error="Recurso no encontrado",
            detalle="La URL solicitada no existe",
            codigo="NOT_FOUND",
        ).model_dump(),
    )


@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(
            error="No autorizado",
            detalle=str(exc.detail) if hasattr(exc, "detail") else "Token invalido o faltante",
            codigo="UNAUTHORIZED",
        ).model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(403)
async def forbidden_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=ErrorResponse(
            error="Acceso denegado",
            detalle="No tienes permisos para acceder a este recurso",
            codigo="FORBIDDEN",
        ).model_dump(),
    )


@app.exception_handler(422)
async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    if hasattr(exc, "errors"):
        errors = exc.errors()
        detalles = [
            {"campo": " -> ".join(str(loc) for loc in e.get("loc", [])), "mensaje": e.get("msg", "")}
            for e in errors
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                error="Error de validacion",
                detalle="Los datos enviados no son validos",
                codigo="VALIDATION_ERROR",
                detalles=detalles,
            ).model_dump(),
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Error de validacion",
            detalle=str(exc),
            codigo="VALIDATION_ERROR",
        ).model_dump(),
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Error interno del servidor",
            detalle="Ha ocurrido un error inesperado",
            codigo="INTERNAL_ERROR",
        ).model_dump(),
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Error de base de datos",
            detalle="Ha ocurrido un error al procesar la solicitud",
            codigo="DATABASE_ERROR",
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Eventos de ciclo de vida
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup() -> None:
    """Inicializa la conexion a la base de datos."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Cierra la conexion a la base de datos."""
    await engine.dispose()


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, Any]:
    return {"status": "ok", "version": "1.0.0"}
