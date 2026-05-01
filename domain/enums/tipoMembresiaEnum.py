"""
Enumeraciones del dominio de ImpactoFit.
"""

import enum

class TipoMembresiaEnum(str, enum.Enum):
    """Tipos de membresía disponibles."""
    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"
