# domain/entities/__init__.py
"""Importa todas las entidades y fuerza configuración de mappers."""

from sqlalchemy.orm import configure_mappers

from .AuditBase import Base
from .Ejercicio import Ejercicio
from .Usuario import Usuario
from .Membresia import Membresia
from .Pago import Pago
from .Rutina import Rutina
from .Ejecucion import Ejecucion
from .Asistencia import Asistencia
from .ClaseGrupal import ClaseGrupal
from .Inscripcion import Inscripcion

# Fuerza resolución de todas las relaciones bidireccionales
configure_mappers()