from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase

class Inscripcion(AuditBase):
    """
    Tabla: inscripciones

    Tabla intermedia entre Cliente y ClaseGrupal.
    Registra qué clientes se inscribieron a qué clases.
    """

    __tablename__ = "inscripciones"

    __table_args__ = (
        UniqueConstraint(
            "usuarioId",
            "claseId",
            name="uq_inscripcion_usuario_clase"
        ),
    )
    usuarioId = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    claseId = Column(Integer, ForeignKey("clasesGrupales.id"), nullable=False)
    fechaInscripcion = Column(DateTime, nullable=False, default=datetime.utcnow)
    cancelada = Column(Boolean, default=False, nullable=False)

    #Relaciones

    usuario = relationship("Usuario", back_populates="inscripciones")
    clase = relationship("ClaseGrupal", back_populates="inscripciones")

    def __repr__(self):
        return (
            f"<Inscripcion "
            f"usuario_id={self.usuarioId} "
            f"clase_id={self.claseId}>"
        )