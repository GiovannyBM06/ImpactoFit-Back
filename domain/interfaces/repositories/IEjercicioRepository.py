"""
IEjercicioRepository.py
-----------------------
Interfaz del repositorio del catálogo de ejercicios.
"""

from abc import abstractmethod
from domain.entities.Ejercicio import Ejercicio
from domain.interfaces.repositories.IGenericRepository import IGenericRepository


class IEjercicioRepository(IGenericRepository[Ejercicio]):

    @abstractmethod
    async def obtenerPorNombre(self, nombre: str) -> Ejercicio | None:
        pass

    @abstractmethod
    async def existeNombre(self, nombre: str) -> bool:
        pass