"""
IEntrenadorRepository.py
------------------------
Interfaz del repositorio de entrenadores.
"""

from abc import abstractmethod
from domain.entities.Usuario import Usuario
from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import Ejecucion
from domain.interfaces.repositories.IGenericRepository import IGenericRepository


class IEntrenadorRepository(IGenericRepository[Usuario]):

    @abstractmethod
    async def obtenerClientesAsignados(self, entrenadorId: int) -> list[Usuario]:
        """Retorna los clientes que tienen una rutina asignada por este entrenador."""
        pass

    @abstractmethod
    async def obtenerRutinaDeCliente(
        self, clienteId: int, entrenadorId: int
    ) -> Rutina | None:
        """
        Retorna la rutina activa de un cliente específico
        verificando que pertenezca a este entrenador.
        """
        pass

    @abstractmethod
    async def crearRutina(self, rutina: Rutina) -> Rutina:
        """Persiste una nueva rutina."""
        pass

    @abstractmethod
    async def agregarEjecucion(self, ejecucion: Ejecucion) -> Ejecucion:
        """Agrega un ejercicio con sus parámetros a una rutina."""
        pass

    @abstractmethod
    async def obtenerEjecucion(self, ejecucionId: int) -> Ejecucion | None:
        """Busca una ejecución por su id."""
        pass

    @abstractmethod
    async def actualizarEjecucion(self, ejecucion: Ejecucion) -> Ejecucion:
        """Persiste los cambios de una ejecución existente."""
        pass

    @abstractmethod
    async def eliminarEjecucion(self, ejecucionId: int) -> bool:
        """Elimina un ejercicio de una rutina."""
        pass