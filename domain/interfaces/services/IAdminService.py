"""
IAdminService.py
----------------
Interfaz del servicio de administradores.

Casos de uso del MVP para el rol ADMINISTRADOR:
    - Ver todos los clientes
    - Ver todas las membresías
    - Crear membresía para un cliente
    - Confirmar pago y activar membresía (Strategy + Observer)
    - Crear clase grupal
    - Asignar entrenador a cliente
    - Desvincular entrenador de cliente
"""

from abc import ABC, abstractmethod
from domain.entities.Usuario import Usuario
from domain.entities.Membresia import Membresia
from domain.entities.Pago import Pago
from domain.entities.ClaseGrupal import ClaseGrupal


class IAdminService(ABC):

    @abstractmethod
    async def verTodosLosClientes(self) -> list[Usuario]:
        pass

    @abstractmethod
    async def verTodasLasMembresias(self) -> list[Membresia]:
        pass

    @abstractmethod
    async def crearMembresia(
        self,
        clienteId: int,
        tipo: str,
    ) -> Membresia:
        """
        Crea una membresía en estado PENDIENTE para un cliente.

        Raises:
            ValueError: si el cliente ya tiene una membresía activa.
        """
        pass

    @abstractmethod
    async def confirmarPagoYActivarMembresia(
        self,
        membresiaId: int,
        adminId: int,
        monto: int,
        notas: str | None = None,
    ) -> Pago:
        """
        Confirma el pago de una membresía y la activa.

        Internamente:
            1. Valida que la membresía existe y está en estado PENDIENTE
            2. Usa Strategy para calcular fechaInicio y fechaVencimiento
            3. Actualiza la membresía a estado ACTIVA
            4. Crea el registro de Pago
            5. Dispara el evento Observer:
                - ComprobanteObserver genera el código de comprobante
                - EstadoUsuarioObserver activa el usuario

        Raises:
            ValueError: si la membresía no existe o no está en estado PENDIENTE.
        """
        pass

    @abstractmethod
    async def crearClaseGrupal(
        self,
        entrenadorId: int,
        nombre: str,
        fechaHora: str,
        cupoMaximo: int,
        descripcion: str | None = None,
    ) -> ClaseGrupal:
        pass

    @abstractmethod
    async def asignarEntrenador(
        self,
        clienteId: int,
        entrenadorId: int,
    ) -> dict:
        """
        Valida que ambos usuarios existan y tengan el rol correcto.

        Raises:
            ValueError: si alguno no existe o tiene rol incorrecto.
        """
        pass

    @abstractmethod
    async def desvincularEntrenador(
        self,
        clienteId: int,
        entrenadorId: int,
    ) -> dict:
        """
        Desactiva la rutina activa que vincula al cliente con el entrenador.

        Raises:
            ValueError: si no existe una rutina activa entre este par.
        """
        pass