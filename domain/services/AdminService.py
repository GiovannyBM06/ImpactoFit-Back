"""
adminService.py
---------------
Implementación del servicio de administradores.

Este es el servicio más importante del MVP en términos de patrones:
    confirmarPagoYActivarMembresia integra Strategy y Observer
    en un flujo cohesivo y desacoplado.

Flujo de confirmarPagoYActivarMembresia:
    1. Validar que la membresía existe y está PENDIENTE
    2. Strategy → calcular fechaVencimiento según tipo de plan
    3. Actualizar membresía a ACTIVA con las fechas calculadas
    4. Crear registro de Pago
    5. Observer → notificar suscriptores:
         - ComprobanteObserver: genera código de comprobante en el Pago
         - EstadoUsuarioObserver: activa el usuario si estaba inactivo
"""

from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.Membresia import Membresia
from domain.entities.Pago import Pago
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Rutina import Rutina
from domain.entities.Usuario import Usuario
from domain.enums.EstadoMembresiaEnum import EstadoMembresiaEnum
from domain.enums.TipoMembresiaEnum import TipoMembresiaEnum
from domain.enums.RolEnum import RolEnum
from domain.interfaces.repositories.IAdminRepository import IAdminRepository
from domain.interfaces.services.IAdminService import IAdminService
from domain.patterns.strategy.IMembresiaStrategy import IMembresiaStrategy
from domain.patterns.observer.MembresiaActivadaEvent import MembresiaActivadaEvent
from domain.patterns.observer.Observadores import (
    ComprobanteObserver,
    EstadoUsuarioObserver,
)
from domain.patterns.observer.IObserver import MembresiaActivadaData


class AdminService(IAdminService):

    def __init__(self, repo: IAdminRepository, db: AsyncSession):
        self._repo = repo
        # La sesión se inyecta directamente para pasarla a los observadores
        self._db = db

    # ── Consultas ─────────────────────────────────────────────────────────────

    async def verTodosLosClientes(self) -> list[Usuario]:
        return await self._repo.obtenerTodosLosClientes()

    async def verTodasLasMembresias(self) -> list[Membresia]:
        return await self._repo.obtenerTodasLasMembresias()
    
    async def verEntrenadores(self) -> list[Usuario]:
        return await self._repo.obtenerEntrenadores()

    # ── Gestión de membresías ─────────────────────────────────────────────────

    async def crearMembresia(
        self,
        clienteId: int,
        tipo: str,
    ) -> Membresia:
        """Crea una membresía en estado PENDIENTE para un cliente."""

        # Verificar que no tenga una membresía activa (RN01)
        membresias = await self._repo.obtenerTodasLasMembresias()
        membresiaActiva = next(
            (
                m for m in membresias
                if m.usuarioID == clienteId
                and m.estado == EstadoMembresiaEnum.ACTIVA
            ),
            None
        )

        if membresiaActiva is not None:
            raise ValueError(
                "El cliente ya tiene una membresía activa. "
                "Debe vencer antes de crear una nueva."
            )

        membresia = Membresia(
            usuarioId=clienteId,
            tipo=TipoMembresiaEnum(tipo.lower()),
            estado=EstadoMembresiaEnum.PENDIENTE,
        )

        return await self._repo.crearMembresia(membresia)

    async def confirmarPagoYActivarMembresia(
        self,
        membresiaId: int,
        adminId: int,
        monto: int,
        notas: str | None = None,
    ) -> Pago:
        """
        Flujo principal del MVP. Integra Strategy + Observer.
        """

        # 1. Validar membresía
        membresia = await self._repo.obtenerMembresiaPorId(membresiaId)

        if membresia is None:
            raise ValueError(f"No se encontró la membresía con id {membresiaId}")

        if membresia.estado != EstadoMembresiaEnum.PENDIENTE:
            raise ValueError(
                f"La membresía está en estado '{membresia.estado}'. "
                f"Solo se pueden activar membresías en estado PENDIENTE."
            )

        # 2. PATRÓN STRATEGY: calcular fechas según tipo de plan
        fechaInicio = date.today()
        strategy = IMembresiaStrategy.obtenerStrategy(membresia.tipo.value)
        fechaVencimiento = strategy.calcularFechaVencimiento(fechaInicio)

        # 3. Actualizar membresía a ACTIVA
        membresia.estado = EstadoMembresiaEnum.ACTIVA
        membresia.fechaInicio = fechaInicio
        membresia.fechaVencimiento = fechaVencimiento
        await self._repo.actualizarMembresia(membresia)

        # 4. Crear registro de Pago
        pago = Pago(
            membresiaId=membresiaId,
            confirmadoPorId=adminId,
            monto=monto,
            fechaPago=datetime.utcnow(),
            notas=notas,
        )
        pago = await self._repo.crearPago(pago)

        # 5. PATRÓN OBSERVER: notificar suscriptores
        evento = MembresiaActivadaEvent()
        evento.suscribir(ComprobanteObserver(self._db))
        evento.suscribir(EstadoUsuarioObserver(self._db))

        data = MembresiaActivadaData(
            membresiaId=membresia.id,
            usuarioId=membresia.usuarioId,
            pagoId=pago.id,
            tipo=membresia.tipo.value,
            fechaInicio=fechaInicio,
            fechaVencimiento=fechaVencimiento,
        )

        await evento.notificar(data)

        return pago

    # ── Gestión de clases grupales ────────────────────────────────────────────

    async def crearClaseGrupal(
        self,
        entrenadorId: int,
        nombre: str,
        fechaHora: str,
        cupoMaximo: int,
        descripcion: str | None = None,
    ) -> ClaseGrupal:

        clase = ClaseGrupal(
            entrenadorId=entrenadorId,
            nombre=nombre,
            fechaHora=datetime.fromisoformat(fechaHora),
            cupoMaximo=cupoMaximo,
            cupoActual=0,
            descripcion=descripcion,
            inscripcionesAbiertas=True,
        )

        return await self._repo.crearClaseGrupal(clase)
    

    async def verTodasLasClases(self) -> list[ClaseGrupal]:
        return await self._repo.obtenerTodasLasClases()


    # ── Gestión de asignaciones ───────────────────────────────────────────────

    async def asignarEntrenador(
        self,
        clienteId: int,
        entrenadorId: int,
    ) -> dict:

        cliente = await self._repo.obtenerPorId(clienteId)
        if cliente is None:
            raise ValueError(f"No se encontró un usuario con id {clienteId}")

        entrenador = await self._repo.obtenerPorId(entrenadorId)
        if entrenador is None:
            raise ValueError(f"No se encontró un usuario con id {entrenadorId}")

        if cliente.rol != RolEnum.CLIENTE:
            raise ValueError(f"El usuario {clienteId} no tiene rol CLIENTE")

        if entrenador.rol != RolEnum.ENTRENADOR:
            raise ValueError(f"El usuario {entrenadorId} no tiene rol ENTRENADOR")

        return {
            "mensaje": (
                f"Entrenador {entrenador.nombre} {entrenador.apellido} "
                f"asignado a {cliente.nombre} {cliente.apellido}. "
                f"Proceda a crear la rutina desde el módulo de entrenamiento."
            ),
            "clienteId":    clienteId,
            "entrenadorId": entrenadorId,
        }

    async def desvincularEntrenador(
        self,
        clienteId: int,
        entrenadorId: int,
    ) -> dict:
        """
        Desvincula al entrenador desactivando la rutina activa
        que los vincula. No elimina la rutina, la deja inactiva
        para preservar el historial del cliente.
        """

        # Buscar la rutina activa que vincula este par
        from sqlalchemy import select
        resultado = await self._db.execute(
            select(Rutina).where(
                Rutina.clienteId == clienteId,
                Rutina.entrenadorId == entrenadorId,
                Rutina.activa == True,
            )
        )
        rutina = resultado.scalar_one_or_none()

        if rutina is None:
            raise ValueError(
                f"No existe una rutina activa que vincule al cliente {clienteId} "
                f"con el entrenador {entrenadorId}."
            )

        rutina.activa = False
        await self._db.commit()

        return {
            "mensaje": (
                f"Entrenador desvinculado del cliente exitosamente. "
                f"La rutina '{rutina.nombre}' fue desactivada."
            ),
            "clienteId":    clienteId,
            "entrenadorId": entrenadorId,
            "rutinaDesactivadaId": rutina.id,
        }