"""
Entidad Membresía. Representa el plan activo de un cliente.
"""

from sqlalchemy import Column, Integer, ForeignKey, Date, Enum, String, Boolean
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase
from domain.enums import TipoMembresiaEnum , EstadoMembresiaEnum

class Membresia(AuditBase):
    """
    Tabla: membresias
    """

    __tablename__ = "membresias"

    usuarioID = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(Enum(TipoMembresiaEnum), nullable=False)
    estado = Column(
        Enum(EstadoMembresiaEnum),
        nullable=False,
        default=EstadoMembresiaEnum.EstadoMembresiaEnum.PENDIENTE
    )
    fechaInicio = Column(Date, nullable=True)
    fechaVencimiento = Column(Date, nullable=True)

    #Relaciones
    pago = relationship(
        "Pago",
        back_populates="membresia",
        uselist=False
    )
    def __repr__(self):
        return (
            f"<Membresia id={self.id} "
            f"tipo={self.tipo} "
            f"estado={self.estado}>"
        )