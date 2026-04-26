"""
membresia.py
------------
Entidad Membresía. Representa el plan activo de un cliente.

Reglas de negocio relacionadas (del Entregable 1):
    RN01 → Un usuario solo puede tener una membresía activa a la vez
    RN02 → Si la membresía está vencida, no se permite el ingreso
    RN04 → El pago debe registrarse antes de activar una membresía
"""

from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, String, Boolean
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase
from domain.enums import MembresíaTipoEnum, MembresíaEstadoEnum


class Membresia(AuditBase):
    """
    Tabla: membresias

    La membresía nace en estado PENDIENTE cuando el administrador la crea.
    Pasa a ACTIVA solo cuando el administrador confirma el pago manualmente.
    El patrón Strategy determina la fecha de vencimiento según el tipo.
    El patrón Observer notifica a los suscriptores cuando se activa.
    """

    __tablename__ = "membresias"

    # Clave foránea al usuario propietario
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Tipo de plan — usado por el patrón Strategy para calcular vencimiento
    tipo = Column(Enum(MembresíaTipoEnum), nullable=False)

    # Estado actual — RN01 y RN02 se validan contra este campo
    estado = Column(
        Enum(MembresíaEstadoEnum),
        nullable=False,
        default=MembresíaEstadoEnum.PENDIENTE
    )

    # Fechas calculadas por la Strategy al momento de activación
    fecha_inicio = Column(Date, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)

    # Comprobante de pago — se genera por el Observer al activar
    comprobante_codigo = Column(String(50), unique=True, nullable=True)
    pago_confirmado = Column(Boolean, default=False, nullable=False)

    # Monto registrado por el administrador al confirmar el pago
    monto_pagado = Column(Integer, nullable=True)  # en pesos colombianos

    # ── Relaciones ──────────────────────────────────────────────────────────

    usuario = relationship("Usuario", back_populates="membresia")

    def __repr__(self):
        return (
            f"<Membresia id={self.id} "
            f"tipo={self.tipo} "
            f"estado={self.estado}>"
        )