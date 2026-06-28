"""
Fixtures de prueba para la plataforma Desenreda.

Usa SQLite en memoria (aiosqlite) como base de datos de prueba.
Parchea el tipo JSONB de PostgreSQL para que funcione con SQLite
a traves de SQLAlchemy compiles.
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import JSON, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB

# ---------------------------------------------------------------------------
# Parche: compilar JSONB como JSON en SQLite
# ---------------------------------------------------------------------------
@compiles(JSONB, "sqlite")
def _compile_jsonb_sqlite(element, compiler, **kw):
    return compiler.visit_JSON(element, **kw)


# ---------------------------------------------------------------------------
# Imports de la aplicacion (despues del parche para evitar errores)
# ---------------------------------------------------------------------------
from app.main import app
from app.database import Base, get_db
from app.models import Usuario, Palabra, Escenario, Frase, Sugerencia
from app.services.auth_service import hash_password, create_access_token

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# ---------------------------------------------------------------------------
# Event loop para pytest-asyncio
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def event_loop():
    """Crea un event loop para toda la sesion de pruebas."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# ---------------------------------------------------------------------------
# Engine de base de datos (sesion completa)
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Crea el engine SQLite en memoria para toda la sesion."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Crear todas las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


# ---------------------------------------------------------------------------
# Sesion de base de datos (por prueba)
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture
async def db_session(test_engine):
    """
    Crea una conexion y transaccion nueva para cada prueba.
    Hace rollback al finalizar para aislar las pruebas.
    """
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = session_maker()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


# ---------------------------------------------------------------------------
# Cliente HTTP asincrono con dependencia override
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP asincrono (httpx) que usa la app FastAPI con la base
    de datos de prueba.
    """

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Usuario de prueba
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> Usuario:
    """Crea un usuario de prueba en la base de datos."""
    usuario = Usuario(
        nombre="Usuario Test",
        email="test@example.com",
        contrasena_hash=hash_password("TestPass123!"),
        preferencias={"tema": "claro"},
    )
    db_session.add(usuario)
    await db_session.flush()
    await db_session.refresh(usuario)
    return usuario


# ---------------------------------------------------------------------------
# Headers de autenticacion (JWT)
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture
async def auth_headers(test_user: Usuario) -> dict[str, str]:
    """Genera headers con token JWT valido para el usuario de prueba."""
    token, _ = create_access_token({"sub": test_user.id})
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Datos de prueba completos
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture
async def seed_test_data(db_session: AsyncSession) -> dict:
    """
    Siembra datos de prueba: escenarios, palabras y frases.
    Retorna un diccionario con referencias a los objetos creados.
    """
    # -- Escenarios -----------------------------------------------------------
    escenario_1 = Escenario(
        nombre="En la calle",
        descripcion="Situaciones cotidianas en la via publica",
        icono="street",
    )
    escenario_2 = Escenario(
        nombre="En el trabajo",
        descripcion="Ambiente laboral chileno",
        icono="work",
    )
    escenario_3 = Escenario(
        nombre="Con amigos",
        descripcion="Conversaciones informales entre amigos",
        icono="friends",
        activo=False,  # Inactivo para probar filtros
    )
    db_session.add_all([escenario_1, escenario_2, escenario_3])
    await db_session.flush()

    # -- Palabras -------------------------------------------------------------
    palabra_1 = Palabra(
        palabra="Weon",
        traduccion="Persona, amigo o tipo. Uso muy versatil.",
        categoria="modismo",
        nivel_formalidad=1.0,
        nivel_ironia=5.0,
        nivel_sarcasmo=4.0,
        pronunciacion_fonetica="we-ON",
        ejemplo_uso="Oye weon, ¿como estas?",
        nota_cultural="Palabra omnipresente en Chile, puede ser amistosa u ofensiva segun el contexto.",
    )
    palabra_2 = Palabra(
        palabra="Pololo",
        traduccion="Novio o pareja sentimental",
        categoria="modismo",
        nivel_formalidad=4.0,
        nivel_ironia=2.0,
        nivel_sarcasmo=1.0,
        pronunciacion_fonetica="po-LO-lo",
        ejemplo_uso="Mi pololo me trajo flores.",
    )
    palabra_3 = Palabra(
        palabra="Cachai",
        traduccion="¿Entiendes? o ¿Captas?",
        categoria="muletilla",
        nivel_formalidad=2.0,
        nivel_ironia=3.0,
        nivel_sarcasmo=2.0,
        ejemplo_uso="Hay que llegar temprano, ¿cachai?",
    )
    palabra_4 = Palabra(
        palabra="Fome",
        traduccion="Aburrido, sin gracia",
        categoria="jerga",
        nivel_formalidad=3.0,
        nivel_ironia=2.0,
        nivel_sarcasmo=1.0,
        ejemplo_uso="La fiesta estuvo fome.",
    )
    db_session.add_all([palabra_1, palabra_2, palabra_3, palabra_4])
    await db_session.flush()

    # -- Frases ---------------------------------------------------------------
    frase_1 = Frase(
        escenario_id=escenario_1.id,
        frase_original="¿Cachai weon?",
        traduccion="¿Entiendes, amigo?",
        explicacion="Pregunta retorica usada para confirmar comprension.",
        tono="informal",
        intencion_real="Confirmar que la otra persona entendio el mensaje.",
        nivel_formalidad=1.0,
        nivel_ironia=3.0,
        nivel_sarcasmo=2.0,
        ejemplo_uso="- Hay que comprar pan, ¿cachai weon? - Si, dale.",
    )
    frase_2 = Frase(
        escenario_id=escenario_2.id,
        frase_original="Estoy al lote",
        traduccion="Estoy desocupado o sin hacer nada productivo",
        explicacion="Expresion usada en contextos laborales informales.",
        tono="informal",
        intencion_real="Indicar que no hay trabajo pendiente.",
        nivel_formalidad=2.0,
        nivel_ironia=1.0,
        nivel_sarcasmo=0.0,
        ejemplo_uso="- ¿Como vas con el informe? - Estoy al lote, ya termine.",
    )
    frase_3 = Frase(
        escenario_id=escenario_2.id,
        frase_original="Pongamosle weno",
        traduccion="Pongamos empeno y trabajemos duro",
        explicacion="Expresion motivacional usada para iniciar o continuar una tarea.",
        tono="motivacional",
        intencion_real="Motivar al equipo a trabajar con energia.",
        nivel_formalidad=4.0,
        nivel_ironia=1.0,
        nivel_sarcasmo=1.0,
        ejemplo_uso="Equipo, pongamosle weno que hay que terminar el proyecto.",
    )
    frase_4 = Frase(
        escenario_id=escenario_1.id,
        frase_original="Echale la culpa al trafico",
        traduccion="Usa el trafico como excusa",
        explicacion="Frase ironica que indica que la persona usa una excusa clasica.",
        tono="ironico",
        intencion_real="Senalar que alguien esta usando una excusa poco creible.",
        nivel_formalidad=3.0,
        nivel_ironia=8.0,
        nivel_sarcasmo=6.0,
        ejemplo_uso="- Llegue tarde porque habia tacos. - Ya, echale la culpa al trafico.",
    )
    db_session.add_all([frase_1, frase_2, frase_3, frase_4])
    await db_session.flush()
    await db_session.refresh(frase_1)
    await db_session.refresh(frase_2)
    await db_session.refresh(frase_3)
    await db_session.refresh(frase_4)

    return {
        "escenario_1": escenario_1,
        "escenario_2": escenario_2,
        "escenario_3": escenario_3,  # inactivo
        "palabra_1": palabra_1,
        "palabra_2": palabra_2,
        "palabra_3": palabra_3,
        "palabra_4": palabra_4,
        "frase_1": frase_1,
        "frase_2": frase_2,
        "frase_3": frase_3,
        "frase_4": frase_4,
    }
