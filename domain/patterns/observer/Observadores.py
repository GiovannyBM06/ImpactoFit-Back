"""
observadores.py
---------------
PATRÓN: Observer — Implementaciones concretas de los suscriptores.

Observadores del evento MembresiaActivada:

    ComprobanteObserver:
        Genera el código único de comprobante de pago.
        Formato: IMP-{AÑO}{MES}-{pagoId:05d}
        Ejemplo: IMP-202504-00042
        Lo asigna al campo comprobanteCodigo del Pago.

    EstadoUsuarioObserver:
        Se asegura de que el usuario quede con isActive = True
        al activar su membresía. Útil si el usuario fue creado
        pero nunca había tenido una membresía activa antes.

Cada observador recibe la sesión de BD por constructor para poder
persistir sus cambios dentro de la misma transacción del servicio.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.patterns.observer.IObserver import IObserver, MembresiaActivadaData
from domain.entities.Pago import Pago
from domain.entities.Usuario import Usuario


class ComprobanteObserver(IObserver):
    """
    Suscriptor que genera el código de comprobante al activar la membresía.
    """

    def __init__(self, db: AsyncSession):
        self._db = db

    async def actualizar(self, data: MembresiaActivadaData) -> None:
        """
        Genera y asigna el código de comprobante al Pago correspondiente.
        """
        pago = await self._db.get(Pago, data.pagoId)
        if pago is None:
            return

        # Formato: IMP-{AÑO}{MES:02d}-{pagoId:05d}
        # Ejemplo: IMP-202504-00042
        pago.comprobanteCodigo = (
            f"IMP-"
            f"{data.fechaInicio.year}"
            f"{data.fechaInicio.month:02d}"
            f"-{data.pagoId:05d}"
        )

        await self._db.commit()
        await self._db.refresh(pago)


class EstadoUsuarioObserver(IObserver):
    """
    Suscriptor que activa el usuario al confirmar su primera membresía.
    """

    def __init__(self, db: AsyncSession):
        self._db = db

    async def actualizar(self, data: MembresiaActivadaData) -> None:
        """
        Garantiza que el usuario quede activo al tener una membresía activa.
        """
        usuario = await self._db.get(Usuario, data.usuarioId)
        if usuario is None:
            return

        if not usuario.isActive:
            usuario.isActive = True
            await self._db.commit()