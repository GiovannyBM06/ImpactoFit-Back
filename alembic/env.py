import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from core.config import settings
from domain.entities.AuditBase import Base

# Importar todas las entidades para que Alembic las detecte
from domain.entities.Usuario import Usuario
from domain.entities.Membresia import Membresia
from domain.entities.Pago import Pago
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Ejercicio import Ejercicio
from domain.entities.Rutina import Rutina
from domain.entities.Asistencia import Asistencia
from domain.entities.Inscripcion import Inscripcion
from domain.entities.Ejecucion import Ejecicion
config = context.config
fileConfig(config.config_file_name)

# Le dice a Alembic qué modelos debe observar para generar migraciones
target_metadata = Base.metadata


def runMigrationsOffline():
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def runMigrationsOnline():
    connectable = create_async_engine(settings.DATABASE_URL)

    async def run():
        async with connectable.connect() as connection:
            await connection.run_sync(
                lambda conn: context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                )
            )
            async with connection.begin():
                await connection.run_sync(
                    lambda conn: context.run_migrations()
                )
        await connectable.dispose()

    asyncio.run(run())

if context.is_offline_mode():
    runMigrationsOffline()
else:
    runMigrationsOnline()