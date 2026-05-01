"""
Clase base abtracta que centraliza los campos comunes a todas la entidades del sistema.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa de SQLAlchemy. Todas las entidades heredan de aquí."""
    pass


class AuditBase(Base):
    """
    Clase base abstracta con campos de auditoría comunes.

    Campos:
        id         → Clave primaria autoincremental
        created_at → Fecha de creación, se asigna automáticamente
        updated_at → Fecha de última modificación, null hasta la primera actualización
    """

    __abstract__ = True  # SQLAlchemy no creará tabla para esta clase

    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow, nullable=True)