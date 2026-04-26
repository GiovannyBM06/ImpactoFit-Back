"""
audit_base.py
-------------
Clase base abstracta para todas las entidades del sistema.
Implementa el principio DRY: define una sola vez los campos comunes
de auditoría que todas las tablas comparten.
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)