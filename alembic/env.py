import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Agregar raíz del proyecto al path para que los imports funcionen
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings
from domain.entities.AuditBase import Base

# Importar todas las entidades para que Alembic las detecte
from domain.entities.Usuario import Usuario
from domain.entities.Membresia import Membresia
from domain.entities.Pago import Pago
from domain.entities.Ejercicio import Ejercicio
from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import Ejecucion
from domain.entities.Asistencia import Asistencia
from domain.entities.ClaseGrupal import ClaseGrupal 
from domain.entities.Inscripcion import Inscripcion

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

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