import enum

class TipoMetricaEnum(str, enum.Enum):
    """
    Define si un ejercicio dentro de una rutina se mide por
    repeticiones o por duración en segundos.
    
    Esta distinción se aplica en la entidad Ejecucion (tabla intermedia
    entre Rutina y Ejercicio). La validación de que solo uno de los dos
    campos esté presente se hace en el schema Pydantic correspondiente.
    """
    REPETICIONES = "repeticiones"
    TIEMPO       = "tiempo"
