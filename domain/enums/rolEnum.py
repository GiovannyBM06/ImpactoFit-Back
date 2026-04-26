"""
enums.py
--------
Enumeraciones del dominio de ImpactoFit.
Centralizadas en un solo archivo por su tamaño reducido en el MVP.
"""

import enum


class RolEnum(str, enum.Enum):
    """Roles posibles de un usuario en el sistema."""
    CLIENTE = "cliente"
    ENTRENADOR = "entrenador"
    ADMINISTRADOR = "administrador"
