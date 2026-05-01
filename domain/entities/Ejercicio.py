from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase

class Ejercicio(AuditBase):
    """
    Tabla: ejercicios

    Un ejercicio pertenece a una rutina específica.
    El entrenador puede agregar, modificar y eliminar ejercicios (MVP).
    """
    __tablename__ = "ejercicios"

    
    nombre = Column(String(150), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    # Relaciones 

    # Un ejercicio puede aparecer en muchas rutinas (a través de Ejecucion)
    ejecuciones = relationship(
        "Ejecucion",
        back_populates="ejercicio",
        cascade="all, delete-orphan"
    )