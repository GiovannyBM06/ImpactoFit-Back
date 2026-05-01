"""
Entidad Pago. Registra la confirmación manual de un pago por parte del admin.

Relación con Membresía:
    Pago tiene la FK hacia Membresia porque es el evento que referencia
    a la membresía existente, no al revés. La membresía puede existir
    sin pago (estado PENDIENTE), pero un pago siempre referencia
    a una membresía concreta.

    Membresia (1) ←── FK ── Pago (1)    [one-to-one]

Flujo completo:
    1. Admin crea la Membresia del cliente → estado: PENDIENTE
    2. Cliente paga por fuera del sistema
    3. Admin registra el Pago en el sistema (este modelo)
    4. Al confirmar el Pago, el servicio activa la Membresia:
         - Strategy calcula fechaVencimiento según tipo
         - Observer notifica suscriptores (comprobante, estado usuario)
         - Membresia.estado → ACTIVA
"""

from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class Pago(AuditBase):
    """
    Tabla: pagos
    Registra un pago confirmado manualmente por un administrador.
    """

    __tablename__ = "pagos"

    # FK a la membresía que este pago activa (one-to-one)
    membresiaId = Column(
        "membresia_id",
        Integer,
        ForeignKey("membresias.id"),
        nullable=False,
        unique=True  # un pago por membresía (one-to-one)
    )

    # FK al administrador que confirmó el pago manualmente
    confirmadoPorId = Column(
        "confirmado_por_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )
    monto = Column(Integer, nullable=False)
    fechaPago = Column(
        "fecha_pago",
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Código único del comprobante generado por el Observer al confirmar
    # Formato sugerido: IMP-{año}{mes}-{id:05d}  ej: IMP-202504-00042
    comprobanteCodigo = Column(
        "comprobante_codigo",
        String(50),
        unique=True,
        nullable=True  # se llena por el Observer, no al crear el registro
    )
    metodoPago = Column(String(50), nullable=True)

    # Relaciones 

    membresia = relationship("Membresia", back_populates="pago")

    confirmadoPorAdmin = relationship(
        "Usuario",
        back_populates="pagosConfirmados",
        foreign_keys=[confirmadoPorId]
    )

    def __repr__(self):
        return (
            f"<Pago id={self.id} "
            f"membresiaId={self.membresiaId} "
            f"monto={self.monto}>"
        )