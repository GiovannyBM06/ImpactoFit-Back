"""
registroAsistencia.py
---------------------
PATRÓN: Template Method — Implementación concreta para registro de asistencia.

Implementa los pasos abstractos de IRegistroTemplate:
    _validarEspecifico() → verifica que el cliente no haya registrado
                           asistencia el día de hoy (evita duplicados)
    _ejecutarAccion()    → crea y persiste el registro de Asistencia

El flujo completo al llamar ejecutar():
    1. _validarCliente()      [IRegistroTemplate] → cliente existe y activo
    2. _validarMembresia()    [IRegistroTemplate] → membresía ACTIVA
    3. _validarEspecifico()   [este archivo]      → sin asistencia hoy
    4. _ejecutarAccion()      [este archivo]      → persiste Asistencia
"""

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.Asistencia import Asistencia
from domain.patterns.template.IRegistroTemplate import IRegistroTemplate


class RegistroAsistencia(IRegistroTemplate):
    """
    Subclase concreta para el registro de ingreso al gimnasio.

    Uso desde ClienteService:
        registro = RegistroAsistencia(db)
        asistencia = await registro.ejecutar(
            clienteId=clienteId,
            observaciones=observaciones
        )
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    # ── Pasos abstractos implementados ───────────────────────────────────────

    async def _validarEspecifico(
        self,
        clienteId: int,
        **kwargs
    ) -> None:
        """
        Verifica que el cliente no haya registrado asistencia hoy.

        Raises:
            ValueError: si ya existe un registro de asistencia para hoy.
        """
        resultado = await self._db.execute(
            select(Asistencia).where(
                Asistencia.usuarioId == clienteId,
                Asistencia.fecha == date.today()
            )
        )
        asistenciaHoy = resultado.scalar_one_or_none()

        if asistenciaHoy is not None:
            raise ValueError(
                "Ya registraste tu asistencia el día de hoy."
            )

    async def _ejecutarAccion(
        self,
        clienteId: int,
        observaciones: str | None = None,
        **kwargs
    ) -> Asistencia:
        """
        Crea y persiste el registro de asistencia.

        Args:
            clienteId     : id del cliente
            observaciones : campo libre del formulario (opcional)

        Returns:
            Asistencia: el registro persistido con id asignado.
        """
        asistencia = Asistencia(
            usuarioId=clienteId,
            fecha=date.today(),
            observaciones=observaciones,
        )

        self._db.add(asistencia)
        await self._db.commit()
        await self._db.refresh(asistencia)

        return asistencia