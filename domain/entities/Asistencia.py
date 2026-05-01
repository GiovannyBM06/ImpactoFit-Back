"""
Entidad Asistencia. Registra cada ingreso de un cliente al gimnasio.
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class Asistencia(AuditBase):
    """
    Tabla: asistencias
    """

    __tablename__ = "asistencias"

    usuarioId = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(Date, nullable=False, default=date.today)
    horaResgistro = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relaciones

    usuario = relationship("Usuario", back_populates="asistencias")

    def __repr__(self):
        return (
            f"<Asistencia id={self.id} "
            f"usuario_id={self.usuarioId} "
            f"fecha={self.fecha}>"
        )