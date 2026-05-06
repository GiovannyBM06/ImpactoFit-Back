"""
IClienteRepository.py
---------------------
Interfaz del repositorio de clientes.

Extiende IGenericRepository[Usuario] con consultas específicas
del contexto de un cliente. El filtro por rol = CLIENTE está
encapsulado en la implementación concreta, invisible para el servicio.
"""

from abc import abstractmethod
from domain.entities.Usuario import Usuario
from domain.entities.Rutina import Rutina
from domain.entities.Asistencia import Asistencia
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Inscripcion import Inscripcion
from domain.interfaces.repositories.IGenericRepository import IGenericRepository


class IClienteRepository(IGenericRepository[Usuario]):

    @abstractmethod
    async def obtenerTodosLosClientes(self) -> list[Usuario]:
        """Retorna todos los usuarios con rol CLIENTE."""
        pass

    @abstractmethod
    async def obtenerRutinaConEjecuciones(self, clienteId: int) -> Rutina | None:
        """
        Retorna la rutina activa del cliente con sus ejecuciones
        y ejercicios cargados (eager loading).
        """
        pass

    @abstractmethod
    async def registrarAsistencia(self, asistencia: Asistencia) -> Asistencia:
        """Persiste un nuevo registro de asistencia."""
        pass

    @abstractmethod
    async def tieneAsistenciaHoy(self, clienteId: int) -> bool:
        """
        Verifica si el cliente ya registró asistencia el día de hoy.
        Evita registros duplicados en el mismo día.
        """
        pass

    @abstractmethod
    async def obtenerClasesDisponibles(self) -> list[ClaseGrupal]:
        """Retorna clases grupales con inscripciones abiertas."""
        pass

    @abstractmethod
    async def obtenerInscripcion(
        self, clienteId: int, claseId: int
    ) -> Inscripcion | None:
        """Busca una inscripción específica de un cliente a una clase."""
        pass

    @abstractmethod
    async def crearInscripcion(self, inscripcion: Inscripcion) -> Inscripcion:
        """Persiste una nueva inscripción."""
        pass

    @abstractmethod
    async def cancelarInscripcion(self, inscripcion: Inscripcion) -> Inscripcion:
        """Marca una inscripción como cancelada."""
        pass