"""
clase_grupal.py
---------------
Entidades ClaseGrupal e Inscripcion.

Regla de negocio (RN05): las clases grupales tienen cupo limitado.
Cuando el cupo se agota, el patrón Observer notifica al sistema
para cerrar nuevas inscripciones automáticamente.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class ClaseGrupal(AuditBase):
    """
    Tabla: clases_grupales

    Creada por el administrador.
    Los clientes se inscriben a través de la app.
    El Observer monitorea cupo_actual vs cupo_max para cerrar inscripciones.
    """

    __tablename__ = "clases_grupales"

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    # Quién dicta la clase
    entrenador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Fecha y hora de la clase
    fecha_hora = Column(DateTime, nullable=False)

    # Control de cupo (RN05)
    cupo_maximo = Column(Integer, nullable=False)
    cupo_actual = Column(Integer, nullable=False, default=0)

    # Cuando cupo_actual == cupo_maximo, el Observer cierra inscripciones
    inscripciones_abiertas = Column(Boolean, default=True, nullable=False)

    # ── Relaciones ──────────────────────────────────────────────────────────

    entrenador = relationship("Usuario", foreign_keys=[entrenador_id])

    inscripciones = relationship(
        "Inscripcion",
        back_populates="clase",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<ClaseGrupal id={self.id} "
            f"nombre={self.nombre} "
            f"cupo={self.cupo_actual}/{self.cupo_maximo}>"
        )


class Inscripcion(AuditBase):
    """
    Tabla: inscripciones

    Tabla intermedia entre Usuario y ClaseGrupal.
    Registra qué clientes se inscribieron a qué clases.
    """

    __tablename__ = "inscripciones"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    clase_id = Column(Integer, ForeignKey("clases_grupales.id"), nullable=False)

    # Fecha en que el cliente se inscribió
    fecha_inscripcion = Column(DateTime, nullable=False, default=datetime.utcnow)

    # El cliente puede cancelar su inscripción
    cancelada = Column(Boolean, default=False, nullable=False)

    # ── Relaciones ──────────────────────────────────────────────────────────

    usuario = relationship("Usuario", back_populates="inscripciones")
    clase = relationship("ClaseGrupal", back_populates="inscripciones")

    def __repr__(self):
        return (
            f"<Inscripcion "
            f"usuario_id={self.usuario_id} "
            f"clase_id={self.clase_id}>"
        )