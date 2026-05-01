import enum

class RolEnum(str, enum.Enum):
    """Roles posibles de un usuario en el sistema."""
    CLIENTE = "cliente"
    ENTRENADOR = "entrenador"
    ADMINISTRADOR = "administrador"
