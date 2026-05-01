import enum

class EstadoMembresiaEnum(str, enum.Enum):
    """
    Estado actual de una membresía.
    Transiciones válidas (Máquina de Estado):
        PENDIENTE → ACTIVA   
        ACTIVA    → VENCIDA
    """
    PENDIENTE = "pendiente"   # Creada pero sin pago confirmado
    ACTIVA = "activa"         # Pago confirmado por administrador
    VENCIDA = "vencida"       # Fecha de vencimiento superada