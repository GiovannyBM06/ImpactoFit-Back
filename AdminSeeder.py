# seed_admin.py
import asyncio
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import configure_mappers  # ← Agregar

from core.config import settings

# ── TRUCO: Importar TODAS las entidades antes de usar cualquiera ──────────────
# Esto garantiza que SQLAlchemy registre todos los mappers en orden correcto

# 1. Primero la base
from domain.entities.AuditBase import Base

# 2. Luego los enums (no dependen de nada)
from domain.enums.RolEnum import RolEnum

# 3. Luego las entidades en orden de dependencia (menos dependientes primero)
from domain.entities.Ejercicio import Ejercicio
from domain.entities.Usuario import Usuario        # Depende de RolEnum
from domain.entities.Membresia import Membresia    # Depende de Usuario, enums
from domain.entities.Pago import Pago              # Depende de Membresia, Usuario
from domain.entities.Rutina import Rutina          # Depende de Usuario
from domain.entities.Ejecucion import Ejecucion    # Depende de Rutina, Ejercicio
from domain.entities.Asistencia import Asistencia # Depende de Usuario
from domain.entities.ClaseGrupal import ClaseGrupal # Depende de Usuario
from domain.entities.Inscripcion import Inscripcion # Depende de Usuario, ClaseGrupal

# 4. Forzar configuración de mappers después de todas las importaciones
configure_mappers()

# ─────────────────────────────────────────────────────────────────────────────

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_NOMBRE   = "Admin"
ADMIN_APELLIDO = "ImpactoFit"
ADMIN_EMAIL    = "admin@impactofit.com"
ADMIN_PASSWORD = "Admin1234"
ADMIN_TELEFONO = None


async def crearAdmin():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )

    async with SessionLocal() as db:
        resultado = await db.execute(
            select(Usuario).where(Usuario.email == ADMIN_EMAIL)
        )
        existente = resultado.scalar_one_or_none()

        if existente is not None:
            print(f"⚠️  Ya existe un usuario con el email '{ADMIN_EMAIL}'.")
            print(f"   Rol actual: {existente.rol.value}")
            return

        admin = Usuario(
            nombre=ADMIN_NOMBRE,
            apellido=ADMIN_APELLIDO,
            email=ADMIN_EMAIL,
            passwordHash=pwdContext.hash(ADMIN_PASSWORD),
            telefono=ADMIN_TELEFONO,
            rol=RolEnum.ADMINISTRADOR,
            isActive=True,
        )

        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        print("✅ Administrador creado exitosamente:")
        print(f"   ID       : {admin.id}")
        print(f"   Nombre   : {admin.nombre} {admin.apellido}")
        print(f"   Email    : {admin.email}")
        print(f"   Rol      : {admin.rol.value}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(crearAdmin())