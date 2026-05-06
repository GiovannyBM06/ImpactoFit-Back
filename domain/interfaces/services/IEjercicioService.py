"""
IEjercicioService.py
--------------------
Interfaz del servicio del catálogo de ejercicios.
"""

from abc import ABC, abstractmethod
from domain.entities.Ejercicio import Ejercicio


class IEjercicioService(ABC):

    @abstractmethod
    async def crearEjercicio(
        self,
        nombre: str,
        descripcion: str | None = None,
    ) -> Ejercicio:
        pass

    @abstractmethod
    async def obtenerTodos(self) -> list[Ejercicio]:
        pass

    @abstractmethod
    async def obtenerPorId(self, ejercicioId: int) -> Ejercicio:
        pass

    @abstractmethod
    async def actualizarEjercicio(
        self,
        ejercicioId: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Ejercicio:
        pass

    @abstractmethod
    async def eliminarEjercicio(self, ejercicioId: int) -> bool:
        pass

    @abstractmethod
    async def buscarPorNombre(self, nombre: str) -> Ejercicio | None:
        pass