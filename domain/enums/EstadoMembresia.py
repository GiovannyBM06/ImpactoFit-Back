import enum

class MembresíaEstadoEnum(str, enum.Enum):
    """Estado actual de una membresía."""
    PENDIENTE = "pendiente"   # Creada pero sin pago confirmado
    ACTIVA = "activa"         # Pago confirmado por administrador
    VENCIDA = "vencida"       # Fecha de vencimiento superada