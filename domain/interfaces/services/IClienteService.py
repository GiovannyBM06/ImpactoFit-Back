"""
IClienteService.py
------------------
Interfaz del servicio de clientes.

Define los casos de uso del MVP correspondientes al rol CLIENTE:
    - Ver su rutina con ejercicios y parámetros
    - Registrar asistencia (con validación de membresía activa)
    - Inscribirse a una clase grupal
    - Cancelar inscripción a una clase grupal
"""

from abc import ABC, abstractmethod
from domain.entities.Rutina import Rutina
from domain.entities.Asistencia import Asistencia
from domain.entities.ClaseGrupal import ClaseGrupal, Inscripcion


class IClienteService(ABC):

    @abstractmethod
    async def verRutina(self, clienteId: int) -> Rutina:
        """
        Retorna la rutina activa del cliente con todos sus ejercicios
        y parámetros de ejecución.

        Raises:
            ValueError: si el cliente no tiene rutina asignada.
        """
        pass

    @abstractmethod
    async def registrarAsistencia(
        self,
        clienteId: int,
        observaciones: str | None = None,
    ) -> Asistencia:
        """
        Registra el ingreso del cliente al gimnasio.

        Validaciones (Template Method en el servicio):
            1. El cliente existe y está activo
            2. Tiene membresía en estado ACTIVA (RN02)
            3. No ha registrado asistencia hoy

        Raises:
            ValueError: si alguna validación falla.
        """
        pass

    @abstractmethod
    async def obtenerClasesDisponibles(self) -> list[ClaseGrupal]:
        """Retorna las clases grupales con cupo disponible."""
        pass

    @abstractmethod
    async def inscribirseAClase(
        self,
        clienteId: int,
        claseId: int,
    ) -> Inscripcion:
        """
        Inscribe al cliente en una clase grupal.

        Validaciones:
            1. El cliente tiene membresía ACTIVA
            2. La clase tiene inscripciones abiertas
            3. El cliente no está ya inscrito

        Raises:
            ValueError: si alguna validación falla.
        """
        pass

    @abstractmethod
    async def cancelarInscripcion(
        self,
        clienteId: int,
        claseId: int,
    ) -> Inscripcion:
        """
        Cancela la inscripción del cliente a una clase grupal.

        Raises:
            ValueError: si no existe la inscripción o ya fue cancelada.
        """
        pass