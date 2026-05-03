"""
IRegistroTemplate.py
--------------------
PATRÓN: Template Method (GoF — Comportamental)

Clase abstracta que define el esqueleto del algoritmo de registro
para operaciones que requieren validación de acceso de un cliente.

Problema que resuelve:
    Tanto el registro de asistencia como la inscripción a una clase
    comparten el mismo flujo de validación:
        1. Verificar que el cliente existe y está activo
        2. Verificar que tiene membresía ACTIVA

    Sin Template Method, ese flujo se duplica en cada servicio.
    Con Template Method, se define una sola vez en la clase abstracta
    y cada subclase solo implementa lo que es diferente.

Estructura del algoritmo (método plantilla: ejecutar()):
    ┌─────────────────────────────────────────────┐
    │  1. await _validarCliente()       [común]   │
    │  2. await _validarMembresia()     [común]   │
    │  3. await _validarEspecifico()    [abstracto]│  ← cada subclase implementa
    │  4. await _ejecutarAccion()       [abstracto]│  ← cada subclase implementa
    └─────────────────────────────────────────────┘

Principios SOLID que satisface:
    OCP → agregar un nuevo tipo de registro (ej: reserva de equipos)
          = nueva subclase, sin modificar el flujo base
    SRP → cada subclase tiene una única responsabilidad
    DRY → la validación común se escribe una sola vez
"""

from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.Usuario import Usuario
from domain.entities.Membresia import Membresia
from domain.enums.EstadoMembresiaEnum import EstadoMembresiaEnum


class IRegistroTemplate(ABC):
    """
    Clase abstracta base del patrón Template Method.

    Define el esqueleto del algoritmo de registro en ejecutar().
    Las subclases concretas implementan _validarEspecifico() y
    _ejecutarAccion() sin alterar el flujo general.

    No se puede instanciar directamente.
    """

    def __init__(self, db: AsyncSession):
        self._db = db
        self._cliente: Usuario | None = None  # se carga en _validarCliente()

    # ── Método plantilla (no se sobreescribe) ────────────────────────────────

    async def ejecutar(self, clienteId: int, **kwargs) -> object:
        """
        Esqueleto del algoritmo. Define el orden fijo de los pasos.

        Este método NO debe ser sobreescrito por las subclases.
        Las subclases implementan los pasos abstractos, no el flujo.

        Args:
            clienteId : id del cliente que realiza la operación
            **kwargs  : parámetros específicos de cada subclase

        Returns:
            El resultado de _ejecutarAccion() (Asistencia o Inscripcion)
        """

        # Paso 1: validación común — cliente existe y está activo
        await self._validarCliente(clienteId)

        # Paso 2: validación común — membresía activa (RN02)
        await self._validarMembresia(clienteId)

        # Paso 3: validación específica de cada subclase
        await self._validarEspecifico(clienteId, **kwargs)

        # Paso 4: acción específica de cada subclase
        return await self._ejecutarAccion(clienteId, **kwargs)

    # ── Pasos comunes (implementados aquí, disponibles para subclases) ───────

    async def _validarCliente(self, clienteId: int) -> None:
        """
        Paso 1: verifica que el cliente existe y está activo.
        Carga el cliente en self._cliente para uso posterior.

        Raises:
            ValueError: si el cliente no existe o está inactivo.
        """
        resultado = await self._db.execute(
            select(Usuario)
            .where(Usuario.id == clienteId)
            .options(selectinload(Usuario.membresia))
        )
        cliente = resultado.scalar_one_or_none()

        if cliente is None:
            raise ValueError(
                f"No se encontró un cliente con id {clienteId}"
            )

        if not cliente.isActive:
            raise ValueError(
                "El cliente no está activo en el sistema"
            )

        # Guardamos el cliente para que las subclases puedan accederlo
        # sin hacer otra query a la BD
        self._cliente = cliente

    async def _validarMembresia(self, clienteId: int) -> None:
        """
        Paso 2: verifica que el cliente tiene membresía ACTIVA (RN02).

        Raises:
            ValueError: si no tiene membresía o no está activa.
        """
        if self._cliente is None:
            raise RuntimeError(
                "_validarMembresia() llamado antes de _validarCliente()"
            )

        if self._cliente.membresia is None:
            raise ValueError(
                "El cliente no tiene membresía asignada. "
                "Comunícate con el administrador."
            )

        if self._cliente.membresia.estado != EstadoMembresiaEnum.ACTIVA:
            raise ValueError(
                f"Tu membresía está en estado "
                f"'{self._cliente.membresia.estado.value}'. "
                f"Se requiere membresía ACTIVA para realizar esta acción."
            )

    # ── Pasos abstractos (cada subclase debe implementarlos) ─────────────────

    @abstractmethod
    async def _validarEspecifico(self, clienteId: int, **kwargs) -> None:
        """
        Paso 3: validación específica de cada tipo de registro.

        RegistroAsistencia  → verifica que no haya asistencia hoy
        RegistroInscripcion → verifica cupo disponible y no inscripción previa
        """
        pass

    @abstractmethod
    async def _ejecutarAccion(self, clienteId: int, **kwargs) -> object:
        """
        Paso 4: acción específica de cada tipo de registro.

        RegistroAsistencia  → crea y persiste el registro de Asistencia
        RegistroInscripcion → crea y persiste la Inscripcion
        """
        pass