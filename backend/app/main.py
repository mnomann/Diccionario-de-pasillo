from fastapi import FastAPI

from app.routers import traducciones_router

app = FastAPI(title="Diccionario de pasillo API")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(traducciones_router, prefix=API_PREFIX)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}


@app.get("/")
def root():
    return {"message": "Diccionario de pasillo API"}
