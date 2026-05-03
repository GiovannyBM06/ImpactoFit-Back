"""
IAdminRepository.py
-------------------
Interfaz del repositorio de administradores.
"""

from abc import abstractmethod
from domain.entities.Usuario import Usuario
from domain.entities.Membresia import Membresia
from domain.entities.Pago import Pago
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.interfaces.repositories.IGenericRepository import IGenericRepository


class IAdminRepository(IGenericRepository[Usuario]):

    @abstractmethod
    async def obtenerTodosLosClientes(self) -> list[Usuario]:
        pass

    @abstractmethod
    async def obtenerTodasLasMembresias(self) -> list[Membresia]:
        pass

    @abstractmethod
    async def obtenerMembresiaPorId(self, membresiaId: int) -> Membresia | None:
        pass

    @abstractmethod
    async def crearMembresia(self, membresia: Membresia) -> Membresia:
        pass

    @abstractmethod
    async def actualizarMembresia(self, membresia: Membresia) -> Membresia:
        pass

    @abstractmethod
    async def crearPago(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    async def crearClaseGrupal(self, clase: ClaseGrupal) -> ClaseGrupal:
        pass

    @abstractmethod
    async def obtenerClasePorId(self, claseId: int) -> ClaseGrupal | None:
        pass

    @abstractmethod
    async def obtenerEntrenadores(self) -> list[Usuario]:
        pass