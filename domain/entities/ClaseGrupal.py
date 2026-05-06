"""
Entidades ClaseGrupal
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class ClaseGrupal(AuditBase):
    """
    Tabla: clases_grupales
    """

    __tablename__ = "clasesGrupales"

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    entrenadorId = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fechaHora = Column(DateTime, nullable=False)
    cupoMaximo = Column(Integer, nullable=False)
    cupoActual = Column(Integer, nullable=False, default=0)
    inscripcionesAbiertas = Column(Boolean, default=True, nullable=False)

    #Relaciones

    entrenador = relationship("Usuario",back_populates="ClasesGrupales" ,foreign_keys=[entrenadorId])

    inscripciones = relationship(
        "Inscripcion",
        back_populates="clase",
        cascade="all, delete-orphan"
    )

    entrenador = relationship(
    "Usuario",
    back_populates="clasesGrupales",  # ← debe coincidir exactamente: clasesGrupales
    foreign_keys=[entrenadorId]
    )
    def __repr__(self):
        return (
            f"<ClaseGrupal id={self.id} "
            f"nombre={self.nombre} "
            f"cupo={self.cupoActual}/{self.cupoMaximo}>"
        )