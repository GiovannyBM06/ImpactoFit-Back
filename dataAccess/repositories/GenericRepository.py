"""
genericRepository.py
--------------------
Implementación base concreta del patrón Repository.

Implementa el contrato IGenericRepository con SQLAlchemy para
las operaciones CRUD estándar. Los repositorios concretos
(UsuarioRepository, MembresiaRepository, etc.) heredan de aquí
y solo agregan los métodos específicos de su entidad.

Beneficio del patrón Repository aquí:
    Si en el futuro se cambia SQLAlchemy por otro ORM, solo se
    modifica este archivo. Los servicios y el dominio no se tocan
    porque dependen de las interfaces, no de esta implementación.
"""

from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from domain.interfaces.repositories.IGenericRepository import IGenericRepository
from domain.entities.AuditBase import AuditBase

T = TypeVar("T", bound=AuditBase)


class GenericRepository(IGenericRepository[T], Generic[T]):
    """
    Implementación CRUD base con SQLAlchemy.

    Los repositorios concretos pasan su entidad al constructor:
        class UsuarioRepository(GenericRepository[Usuario]):
            def __init__(self, db: Session):
                super().__init__(db, Usuario)
    """

    async def __init__(self, db: Session, modelo: Type[T]):
        """
        Args:
            db     : Sesión de SQLAlchemy inyectada por FastAPI (Depends)
            modelo : La clase de la entidad que gestiona este repositorio
        """
        self._db = db
        self._modelo = modelo

    # ── IGenericRepository implementation ────────────────────────────────────

    async def obtenerPorId(self, id: int) -> T | None:
        return await self._db.query(self._modelo).filter(
            self._modelo.id == id
        ).first()

    async def obtenerTodos(self) -> list[T]:
        return await self._db.query(self._modelo).all()

    async def crear(self, entidad: T) -> T:
        self._db.add(entidad)
        await self._db.commit()
        await self._db.refresh(entidad)
        return entidad

    async def actualizar(self, entidad: T) -> T:
        await self._db.commit()
        await self._db.refresh(entidad)
        return entidad

    async def eliminar(self, id: int) -> bool:
        entidad = await self.obtenerPorId(id)
        if entidad is None:
            return False
        await self._db.delete(entidad)
        await self._db.commit()
        return True