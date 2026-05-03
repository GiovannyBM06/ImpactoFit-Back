"""
IGenericRepository.py
---------------------
Interfaz genérica base para todos los repositorios del sistema.

Propósito:
    Define el contrato CRUD mínimo que cualquier repositorio debe cumplir,
    independientemente de la entidad que gestione.

    Al usar TypeVar (T), esta interfaz es reutilizable para cualquier
    entidad que herede de AuditBase (Usuario, Membresia, Pago, Rutina, etc.)

Principios SOLID que satisface:
    ISP → cada repositorio concreto implementa solo lo que necesita,
          y puede extender este contrato con métodos específicos
    DIP → los servicios dependen de esta abstracción, nunca de
          implementaciones concretas de SQLAlchemy
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# T representa cualquier entidad del dominio (Usuario, Membresia, etc.)
T = TypeVar("T")


class IGenericRepository(ABC, Generic[T]):
    """
    Contrato base para todos los repositorios.

    Define las operaciones CRUD estándar que todo repositorio debe exponer.
    Las implementaciones concretas heredan de esta interfaz y de
    GenericRepository (la implementación base en data_access).
    """

    @abstractmethod
    async def obtenerTodos(self) -> list[T]:
        pass

    @abstractmethod
    async def obtenerPorId(self, id: int) -> T | None:
        pass

    @abstractmethod
    async def crear(self, entidad: T) -> T:
        pass

    @abstractmethod
    async def actualizar(self, entidad: T) -> T:
        pass

    @abstractmethod
    async def eliminar(self, id: int) -> bool:
        pass