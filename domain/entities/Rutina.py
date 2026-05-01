"""
Entidad Rutina

"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class Rutina(AuditBase):
    """
    Tabla: rutinas

    Regla de negocio (RN03): solo entrenadores pueden asignar/modificar rutinas.
    Esta validación se aplica en el servicio, no en la entidad.
    """

    __tablename__ = "rutinas"

    clienteID = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    entrenadorID = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activa = Column(Boolean, default=True, nullable=False)

    #Relaciones 

    cliente = relationship(
        "Usuario",
        back_populates="rutina",
        foreign_keys=[clienteID]
    )

    entrenador = relationship(
        "Usuario",
        back_populates="rutinasCreadas",
        foreign_keys=[entrenadorID]
    )

    ejeciciones = relationship(
        "Ejecucion",
        back_populates="rutina",
        cascade= "all, delete-orphan",
        order_by="Ejecucion.orden"
    )
    def __repr__(self):
        return f"<Rutina id={self.id} nombre={self.nombre}  activa ={self.activa}>"
