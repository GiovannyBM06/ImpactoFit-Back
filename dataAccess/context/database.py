"""
database.py
-----------
Configuración asíncrona de la conexión a NeonDB (PostgreSQL serverless).

Cambios respecto a la versión síncrona:
    - create_engine       → create_async_engine
    - sessionmaker        → async_sessionmaker  con  AsyncSession
    - psycopg2-binary     → asyncpg  (driver asíncrono)
    - URL: postgresql://  → postgresql+asyncpg://
    - getDb()             → generador asíncrono con  AsyncSession

Por qué async aquí es importante:
    NeonDB es una BD externa (red). Cada query implica esperar
    una respuesta a través de internet. Con AsyncSession ese tiempo
    de espera no bloquea el servidor: FastAPI puede atender otras
    peticiones mientras espera la respuesta de NeonDB.
"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from core.config import settings
from typing import AsyncGenerator
# ── Engine asíncrono (instancia única / Singleton implícito) ─────────────────

engine = create_async_engine(
    settings.DATABASE_URL,          # debe usar postgresql+asyncpg://

    # Verifica la conexión antes de usarla del pool.
    # Crítico para NeonDB serverless: evita errores por conexiones suspendidas.
    pool_pre_ping=True,

    # Descarta conexiones después de 5 minutos de inactividad.
    pool_recycle=300,

    # Conexiones permanentes en el pool.
    pool_size=5,

    # Conexiones extra cuando el pool está lleno.
    max_overflow=10,

    # Muestra queries SQL en consola. Solo en desarrollo.
    echo=settings.DEBUG,
)


# ── Fábrica de sesiones asíncronas ───────────────────────────────────────────

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # evita queries adicionales al acceder a
                             # atributos después del commit
)


# ── Dependency para FastAPI (Depends) ────────────────────────────────────────

async def getDb() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()