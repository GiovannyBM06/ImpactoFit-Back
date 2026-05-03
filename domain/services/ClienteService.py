"""
clienteService.py
-----------------
Implementación del servicio de clientes.

Implementa IClienteService con los casos de uso del MVP para el rol CLIENTE.

Patrón Template Method aplicado:
    registrarAsistencia e inscribirseAClase comparten el mismo flujo base:
        1. Validar que el cliente existe y está activo
        2. Validar que tiene membresía ACTIVA
        3. Ejecutar la acción específica
        4. Retornar resultado

    En lugar de duplicar ese flujo, _validarAccesoCliente() centraliza
    los pasos 1 y 2. Cada método llama a este validador antes de su
    lógica específica. Es una aplicación simplificada del Template Method
    sin necesidad de clase abstracta, apropiada para este contexto.
"""

from datetime import date

from domain.entities.Rutina import Rutina
from domain.entities.Asistencia import Asistencia
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Inscripcion import Inscripcion
from domain.enums.EstadoMembresiaEnum import EstadoMembresiaEnum
from domain.interfaces.repositories.IClienteRepository import IClienteRepository
from domain.interfaces.services.IClienteService import IClienteService


class ClienteService(IClienteService):

    def __init__(self, repo: IClienteRepository):
        self._repo = repo

    # ── Validador compartido (Template Method simplificado) ──────────────────

    async def _validarAccesoCliente(self, clienteId: int) -> None:
        """
        Valida que el cliente pueda realizar operaciones en el sistema.
        Usado como paso común en registrarAsistencia e inscribirseAClase.

        Raises:
            ValueError: si el cliente no existe, está inactivo
                        o no tiene membresía activa.
        """
        cliente = await self._repo.obtenerPorId(clienteId)

        if cliente is None:
            raise ValueError(f"No se encontró un cliente con id {clienteId}")

        if not cliente.isActive:
            raise ValueError("El cliente no está activo en el sistema")

        if cliente.membresia is None:
            raise ValueError("El cliente no tiene membresía asignada")

        if cliente.membresia.estado != EstadoMembresiaEnum.ACTIVA:
            raise ValueError(
                f"La membresía del cliente está en estado "
                f"'{cliente.membresia.estado}'. "
                f"Se requiere membresía ACTIVA para realizar esta acción"
            )

    # ── Casos de uso ─────────────────────────────────────────────────────────

    async def verRutina(self, clienteId: int) -> Rutina:
        rutina = await self._repo.obtenerRutinaConEjecuciones(clienteId)

        if rutina is None:
            raise ValueError(
                "No tienes una rutina activa asignada. "
                "Comunícate con tu entrenador."
            )

        return rutina

    async def registrarAsistencia(
        self,
        clienteId: int,
        observaciones: str | None = None,
    ) -> Asistencia:
        """
        Template Method:
            1. _validarAccesoCliente() → valida existencia y membresía
            2. Verifica que no haya asistencia registrada hoy
            3. Crea y persiste el registro
        """

        # Paso 1: validación común
        await self._validarAccesoCliente(clienteId)

        # Paso 2: validación específica de asistencia
        if await self._repo.tieneAsistenciaHoy(clienteId):
            raise ValueError("Ya registraste tu asistencia el día de hoy")

        # Paso 3: registrar
        asistencia = Asistencia(
            usuarioId=clienteId,
            fecha=date.today(),
            observaciones=observaciones,
        )

        return await self._repo.registrarAsistencia(asistencia)

    async def obtenerClasesDisponibles(self) -> list[ClaseGrupal]:
        return await self._repo.obtenerClasesDisponibles()

    async def inscribirseAClase(
        self,
        clienteId: int,
        claseId: int,
    ) -> Inscripcion:
        """
        Template Method:
            1. _validarAccesoCliente() → valida existencia y membresía
            2. Verifica que la clase tenga cupo
            3. Verifica que no esté ya inscrito
            4. Crea la inscripción
        """

        # Paso 1: validación común
        await self._validarAccesoCliente(clienteId)

        # Paso 2: verificar cupo
        clases = await self._repo.obtenerClasesDisponibles()
        clase = next((c for c in clases if c.id == claseId), None)

        if clase is None:
            raise ValueError(
                "La clase no existe o no tiene inscripciones abiertas"
            )

        # Paso 3: verificar inscripción previa
        inscripcionExistente = await self._repo.obtenerInscripcion(
            clienteId, claseId
        )
        if inscripcionExistente is not None:
            raise ValueError("Ya estás inscrito en esta clase")

        # Paso 4: crear inscripción
        inscripcion = Inscripcion(
            usuarioId=clienteId,
            claseId=claseId,
        )

        return await self._repo.crearInscripcion(inscripcion)

    async def cancelarInscripcion(
        self,
        clienteId: int,
        claseId: int,
    ) -> Inscripcion:
        inscripcion = await self._repo.obtenerInscripcion(clienteId, claseId)

        if inscripcion is None:
            raise ValueError(
                "No se encontró una inscripción activa para esta clase"
            )

        return await self._repo.cancelarInscripcion(inscripcion)