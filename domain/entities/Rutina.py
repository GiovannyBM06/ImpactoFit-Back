"""
rutina.py
---------
Entidades Rutina y Ejercicio.

Relación: una Rutina tiene múltiples Ejercicios.
El entrenador crea y modifica la rutina de su cliente asignado.
El cliente solo puede consultar su rutina (solo lectura).
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class Rutina(AuditBase):
    """
    Tabla: rutinas

    Una rutina pertenece a un cliente y es gestionada por un entrenador.
    Contiene una colección de ejercicios ordenados.

    Regla de negocio (RN03): solo entrenadores pueden asignar/modificar rutinas.
    Esta validación se aplica en el servicio, no en la entidad.
    """

    __tablename__ = "rutinas"

    # El cliente al que pertenece esta rutina
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # El entrenador que la gestiona
    entrenador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activa = Column(Boolean, default=True, nullable=False)

    # ── Relaciones ──────────────────────────────────────────────────────────

    cliente = relationship(
        "Usuario",
        back_populates="rutina",
        foreign_keys=[cliente_id]
    )

    entrenador = relationship(
        "Usuario",
        back_populates="rutinas_asignadas",
        foreign_keys=[entrenador_id]
    )

    # Una rutina tiene múltiples ejercicios
    ejercicios = relationship(
        "Ejercicio",
        back_populates="rutina",
        cascade="all, delete-orphan",  # si se borra la rutina, se borran sus ejercicios
        order_by="Ejercicio.orden"
    )

    def __repr__(self):
        return f"<Rutina id={self.id} nombre={self.nombre}>"


class Ejercicio(AuditBase):
    """
    Tabla: ejercicios

    Un ejercicio pertenece a una rutina específica.
    El entrenador puede agregar, modificar y eliminar ejercicios (MVP).
    """

    __tablename__ = "ejercicios"

    rutina_id = Column(Integer, ForeignKey("rutinas.id"), nullable=False)

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    series = Column(Integer, nullable=False)
    repeticiones = Column(Integer, nullable=False)
    descanso_segundos = Column(Integer, nullable=True, default=60)

    # Orden de aparición dentro de la rutina
    orden = Column(Integer, nullable=False, default=1)

    # ── Relaciones ──────────────────────────────────────────────────────────

    rutina = relationship("Rutina", back_populates="ejercicios")

    def __repr__(self):
        return (
            f"<Ejercicio id={self.id} "
            f"nombre={self.nombre} "
            f"series={self.series}x{self.repeticiones}>"
        )